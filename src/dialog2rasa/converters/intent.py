from pathlib import Path

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_to_file


class IntentConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        language: str,
    ) -> None:
        super().__init__(agent_dir, language)

    def convert(self) -> None:
        """Converts Dialogflow intents to Rasa NLU format."""
        converted_intents = self._gather_intent_data()
        write_to_file(self.nlu_output_path, converted_intents)
        logger.debug(f"The file '{self.nlu_output_path}' has been created.")

    def _gather_intent_data(self) -> str:
        """Gathers intent data and converts it into Rasa format."""
        converted_intents = 'version: "3.1"\n\nnlu:\n'
        intent_file_stem = f"_usersays_{self.language}"

        for file in sorted(self.intents_dir.glob(f"*{intent_file_stem}.json")):
            intent_name = camel_to_snake(file.stem.split(intent_file_stem)[0])
            data = read_json_file(file)
            examples = self._gather_example_data(data)
            converted_intents += (
                f"  - intent: {intent_name}\n    examples: |\n{examples}\n"
            )

        return converted_intents

    def _gather_example_data(self, data: dict) -> str:
        """Gathers example data and converts it into Rasa format."""
        examples = ""
        for d in data:
            text = "".join(
                (
                    f'[{fragment["text"]}]'
                    f'({fragment["meta"].replace("@", "").replace(".", "_")})'
                    if "meta" in fragment
                    else fragment["text"]
                )
                for fragment in d["data"]
            )
            examples += f"      - {text.strip()}\n"
        return examples
