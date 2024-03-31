from pathlib import Path

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_dict_files, write_to_file


class EntityConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        language: str,
    ) -> None:
        super().__init__(agent_dir, language)

    def convert(self) -> None:
        """Processes and converts Dialogflow entities to Rasa format."""
        entity_contents = self._handle_entities()
        for entity_dict in entity_contents:
            write_dict_files(entity_dict)

        self._append_entities_as_slots()

        logger.debug(
            f"The entity files have been created in dir '{self.nlu_folder_dir}'."
        )

    def _handle_entities(
        self,
    ) -> tuple[dict[Path, str], dict[Path, str], dict[Path, str]]:
        """
        Handles entities of different kinds, returning a with all three types below:

        1) Compound entities: stored in __compound__{entity_name}.yml for user
        review, since not they are not Rasa-compatible;
        2) Entities with more than one synonym are stored under synonyms in nlu.yaml;
        3) Entities with one  one value are stored in lookup tables;
        """
        self.synonym_content, self.lookup_content, self.compound_content = {}, {}, {}

        for entity_file in self.entities_dir.glob(f"*_entries_{self.language}.json"):
            entity_name = camel_to_snake(entity_file.stem).replace(
                f"_entries_{self.language}", ""
            )
            entries = read_json_file(entity_file)

            for entry in entries:
                if any("@" in syn for syn in entry["synonyms"]):
                    self._process_compound_entity(entry, entity_name)
                elif len(entry["synonyms"]) > 1:
                    self._process_synonym_entity(entry)
                else:
                    self._process_lookup_entity(entry, entity_name)

        return self.synonym_content, self.lookup_content, self.compound_content

    def _append_entities_as_slots(self) -> None:
        """Handles entities as slots and appends them to the domain file."""
        slot_entities_content = self._process_entities_as_slots()
        if slot_entities_content:
            write_to_file(self.domain_file_path, slot_entities_content, "a")
            logger.warning(
                "Entities have been added as slots to the domain file. "
                "Please review slot types and mappings."
            )

    def _process_compound_entity(self, entry: dict, entity_name: str) -> None:
        compound_file_path = self.nlu_folder_dir / f"__compound__{entity_name}.yml"
        if compound_file_path not in self.compound_content:
            self.compound_content[compound_file_path] = (
                self._init_compound_file_content()
            )
            logger.warning(
                "Manual adaptation needed for compound "
                f"entity '{entity_name}' in Rasa. "
                f"See file: '__compound__{entity_name}.yml'."
            )
        self._update_content(
            self.compound_content,
            compound_file_path,
            self._handle_compounds(entry),
        )

    def _process_synonym_entity(self, entry: dict) -> None:
        self._update_content(
            self.synonym_content,
            self.nlu_output_path,
            self._handle_synonyms(entry),
        )

    def _process_lookup_entity(self, entry: dict, entity_name: str) -> None:
        lookup_file_path = self.lookup_dir / f"{entity_name}.txt"
        self._update_content(
            self.lookup_content,
            lookup_file_path,
            self._handle_lookup(entry),
        )

    def _update_content(self, content_dict: dict, file_path: Path, new_content: str):
        if file_path not in content_dict:
            content_dict[file_path] = ""
        content_dict[file_path] += new_content

    def _handle_synonyms(self, entry: dict) -> str:
        """Returns Rasa format string for Dialogflow synonyms."""
        synonym = entry["value"]
        examples = "\n".join(f"      - {syn}" for syn in entry["synonyms"])
        return f"  - synonym: {synonym}\n    examples: |\n{examples}\n\n"

    def _handle_lookup(self, entry: dict) -> str:
        """Returns Rasa format string for Dialogflow lookup tables."""
        return "\n".join(entry["synonyms"]) + "\n"

    def _init_compound_file_content(self) -> str:
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

    def _process_entities_as_slots(self) -> str:
        """Returns entities as slots for appending to the Rasa domain file."""
        if not self.domain_file_path.exists():
            logger.error(f"Domain file {self.domain_file_path} not found.")
            return ""

        entity_names = sorted(
            set(
                [
                    x.stem.split("_entries")[0]
                    for x in self.entities_dir.glob(f"*_entries_{self.language}.json")
                ]
            )
        )
        entities_str = "\n  - ".join(entity_names)
        slots_str = "\n".join(
            f"  {entity_name}:\n    type: text\n    "
            "influence_conversation: false\n    mappings:\n    "
            f"- type: from_entity\n      entity: {entity_name}\n"
            for entity_name in entity_names
        )

        return (
            "# TODO: Review assumption of Dialogflow "
            "entities as slots and entities. "
            "Confirm the types and mappings.\nentities:"
            f"\n  - {entities_str}\n\nslots:\n{slots_str}\n"
        )
