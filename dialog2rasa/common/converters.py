import re
from abc import abstractmethod

from common.io import read_json_file, write_dict_files, write_to_file
from common.loggers import logger


def camel_to_snake(s: str) -> str:
    """Converts input string from CamelCase to snake_case."""
    return (
        re.sub(r"(?<!^)(?=[A-Z])", "_", s)  # insert underscores before capital letters
        .replace(" ", "_")  # fix non non-standard CamelCase inputs
        .replace("__", "_")  # fix double underscores (from previous replace)
        .lower()  # lowercase for true snake_case
    )


class BaseConverter:
    """
    Base converter to simplify initialization. Main function are:
    1) Manipulate the strings from Dialogflow export files and;
    2) Export the output files following the RASA YAML-format.
    """

    def __init__(self, agent_dir, agent_name, languages, output_file=None, sub_dir=""):
        self.agent_dir = agent_dir
        self.agent_name = agent_name
        self.languages = languages
        self.base_output_path = agent_dir / "output"
        self.nlu_folder_path = (
            self.base_output_path / "data" / "nlu"
            if sub_dir == "nlu"
            else self.base_output_path
        )
        self.output_file = output_file if output_file else f"{self.agent_name}.yml"
        self.output_path = self.nlu_folder_path / self.output_file

    @abstractmethod
    def convert(self) -> None: ...


class IntentConverter(BaseConverter):
    def __init__(self, agent_dir, agent_name, languages, output_file=None):
        super().__init__(agent_dir, agent_name, languages, output_file, "nlu")
        self.intents_path = agent_dir / "intents"

    def convert(self) -> None:
        """Converts Dialogflow intents to Rasa NLU format."""
        converted_intents = self._handle_intents()
        write_to_file(self.output_path, converted_intents)
        logger.info(f"The file '{self.output_path}' has been created.")

    def _handle_intents(self) -> str:
        """Handles conversion of individual Dialogflow intents."""
        converted_intents = 'version: "3.1"\n\nnlu:\n'
        for lang in self.languages:
            intent_file_stem = f"_usersays_{lang}"

            for file in sorted(self.intents_path.glob(f"*{intent_file_stem}.json")):
                intent_name = camel_to_snake(file.stem.split(intent_file_stem)[0])
                data = read_json_file(file)
                examples = self._handle_examples(data)
                converted_intents += (
                    f"  - intent: {intent_name}\n    examples: |\n{examples}\n"
                )

        return converted_intents

    def _handle_examples(self, data: dict) -> str:
        """Handles conversion of Dialogflow examples to Rasa format."""
        examples = ""
        for d in data:
            text = "".join(
                (
                    f'[{fragment["text"]}]({fragment["meta"].replace("@", "").replace(".", "_")})'
                    if "meta" in fragment
                    else fragment["text"]
                )
                for fragment in d["data"]
            )
            examples += f"      - {text.strip()}\n"
        return examples


class UtteranceConverter(BaseConverter):
    def __init__(self, agent_dir, agent_name, languages, output_file="domain.yml"):
        super().__init__(agent_dir, agent_name, languages, output_file)

    def convert(self) -> None:
        """Converts Dialogflow utterances to Rasa domain format."""
        responses_folder_path = self.agent_dir / "intents"
        converted_responses = self._handle_responses(responses_folder_path)
        write_to_file(self.output_path, converted_responses)
        logger.info(f"The file '{self.output_path}' has been created.")

    def _handle_responses(self, responses_folder_path) -> str:
        """Handles conversion of Dialogflow responses to Rasa format."""
        converted_responses = "responses:\n"
        for file in sorted(responses_folder_path.iterdir()):
            if not any(
                file.name.endswith(f"usersays_{lang}.json") for lang in self.languages
            ):
                intent_name = camel_to_snake(file.stem)
                data = read_json_file(file)
                for response in data.get("responses", []):
                    converted_responses += self._handle_utter_message(
                        intent_name, response
                    )
        return converted_responses

    def _handle_utter_message(self, intent_name, response) -> str:
        """Handles conversion of individual Dialogflow utter messages."""
        converted_utter = ""
        for message in response.get("messages", []):
            if message.get("lang") in self.languages:
                if "speech" in message:
                    converted_utter += f"  utter_{intent_name}:\n"
                    for s in message["speech"]:
                        converted_utter += f'    - text: "{s}"\n'
                    converted_utter += "\n"
        return converted_utter


class EntityConverter(BaseConverter):
    def __init__(self, agent_dir, agent_name, languages, output_file=None):
        super().__init__(agent_dir, agent_name, languages, output_file, "nlu")
        self.lookup_path = self.nlu_folder_path / "lookup"
        self.entities_path = self.agent_dir / "entities"

    def convert(self) -> None:
        """Processes and converts Dialogflow entities to Rasa format."""
        entity_contents = self._handle_entities()
        for entity_dict in entity_contents:
            write_dict_files(entity_dict)
        logger.info(
            f"The entity files have been created in dir '{self.nlu_folder_path}'."
        )

    def _handle_entities(self) -> tuple:
        synonym_content, lookup_content, compound_content = {}, {}, {}

        for lang in self.languages:
            for entity_file in self.entities_path.glob(f"*_entries_{lang}.json"):
                entity_name = camel_to_snake(entity_file.stem).replace(
                    f"_entries_{lang}", ""
                )
                entries = read_json_file(entity_file)

                for entry in entries:
                    if any("@" in syn for syn in entry["synonyms"]):
                        # @ refers to compound entities in dialogflow
                        compound_file_path = (
                            self.nlu_folder_path / f"__compound__{entity_name}.yml"
                        )
                        if compound_file_path not in compound_content:
                            compound_content[compound_file_path] = (
                                self._init_compound_file_content(entity_name)
                            )
                            logger.warning(
                                "Manual adaptation needed for compound "
                                f"entity '{entity_name}' in Rasa. "
                                f"See file: '__compound__{entity_name}.yml'."
                            )
                        self._update_content(
                            compound_content,
                            compound_file_path,
                            self._handle_compounds(entry),
                        )

                    elif len(entry["synonyms"]) > 1:
                        # multiple synonyms are considered also synonyms in RASA
                        synonyms_file_path = (
                            self.nlu_folder_path / f"{self.agent_name}.yml"
                        )
                        self._update_content(
                            synonym_content,
                            synonyms_file_path,
                            self._handle_synonyms(entry),
                        )

                    else:
                        # single synonyms are accumulated in lookup tables
                        lookup_file_path = self.lookup_path / f"{entity_name}.txt"
                        self._update_content(
                            lookup_content,
                            lookup_file_path,
                            self._handle_lookup(entry, entity_name),
                        )

        return synonym_content, lookup_content, compound_content

    def _update_content(self, content_dict, file_path, new_content):
        if file_path not in content_dict:
            content_dict[file_path] = ""
        content_dict[file_path] += new_content

    def _handle_synonyms(self, entry: dict) -> str:
        """Returns Rasa format string for Dialogflow synonyms."""
        synonym = entry["value"]
        examples = "\n".join(f"    - {syn}" for syn in entry["synonyms"])
        return f"- synonym: {synonym}\n  examples: |\n{examples}\n\n"

    def _handle_lookup(self, entry: dict, entity_name: str) -> str:
        """Returns Rasa format string for Dialogflow lookup tables."""
        return "\n".join(entry["synonyms"]) + "\n"

    def _init_compound_file_content(self, entity_name: str) -> str:
        """Returns the initial content for a new compound entity file."""
        header_content = "# Compound entity: Manual adaptation needed for Rasa\n"
        header_content += 'version: "3.1"\n\nnlu:\n'
        return header_content

    def _handle_compounds(self, entry: dict) -> str:
        """
        Returns Rasa format string for pseudo-compound entities from Dialogflow.
        No need to check for new files here, handled in convert method.
        """
        synonym = entry["value"]
        examples = "\n".join(f"      - {syn}" for syn in entry["synonyms"])
        return f"  - synonym: {synonym}\n    examples: |\n{examples}\n\n"


def get_converter(type_: str, *args, **kwargs) -> BaseConverter:
    converters = {
        "intent": IntentConverter,
        "utterance": UtteranceConverter,
        "entity": EntityConverter,
    }
    return converters[type_](*args, **kwargs)
