from pathlib import Path

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.formatting import (
    format_compounds_for_rasa,
    format_lookup_for_rasa,
    format_synonyms_for_rasa,
    initialize_compound_file_header,
)
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_dict_files


class EntityConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        language: str,
    ) -> None:
        super().__init__(agent_dir, language)

    def convert(self) -> None:
        """Processes and converts Dialogflow entities to Rasa format."""
        entity_contents = self._gather_entity_data()
        for entity_dict in entity_contents:
            write_dict_files(entity_dict)

        logger.debug(
            f"The entity files have been created in dir '{self.nlu_folder_dir}'."
        )

    def _gather_entity_data(
        self,
    ) -> tuple[dict[Path, str], dict[Path, str], dict[Path, str]]:
        """
        Gathers entity data of the three different kinds below:

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
                    self._create_compound_entity_records(entry, entity_name)
                elif len(entry["synonyms"]) > 1:
                    self._create_synonym_entity_records(entry)
                else:
                    self._create_lookup_entity_records(entry, entity_name)

        return self.synonym_content, self.lookup_content, self.compound_content

    def _create_compound_entity_records(self, entry: dict, entity_name: str) -> None:
        compound_file_path = self.nlu_folder_dir / f"__compound__{entity_name}.yml"
        if compound_file_path not in self.compound_content:
            self.compound_content[compound_file_path] = (
                initialize_compound_file_header()
            )
            logger.warning(
                "Manual adaptation needed for compound "
                f"entity '{entity_name}' in Rasa. "
                f"See file: '__compound__{entity_name}.yml'."
            )
        self._append_to_file_content(
            self.compound_content,
            compound_file_path,
            format_compounds_for_rasa(entry),
        )

    def _create_synonym_entity_records(self, entry: dict) -> None:
        self._append_to_file_content(
            self.synonym_content,
            self.nlu_output_path,
            format_synonyms_for_rasa(entry),
        )

    def _create_lookup_entity_records(self, entry: dict, entity_name: str) -> None:
        lookup_file_path = self.lookup_dir / f"{entity_name}.txt"
        self._append_to_file_content(
            self.lookup_content,
            lookup_file_path,
            format_lookup_for_rasa(entry),
        )

    def _append_to_file_content(
        self, content_dict: dict, file_path: Path, new_content: str
    ):
        if file_path not in content_dict:
            content_dict[file_path] = ""
        content_dict[file_path] += new_content
