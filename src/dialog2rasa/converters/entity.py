from pathlib import Path
from typing import Optional

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_dict_files


class EntityConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        agent_name: str,
        language: str,
        output_file: Optional[str] = None,
    ) -> None:
        super().__init__(agent_dir, agent_name, language, output_file, "nlu")
        self.lookup_path = self.nlu_folder_path / "lookup"
        self.entities_path = self.agent_dir / "entities"

    def convert(self) -> None:
        """Processes and converts Dialogflow entities to Rasa format."""
        entity_contents = self._handle_entities()
        for entity_dict in entity_contents:
            write_dict_files(entity_dict)
        logger.debug(
            f"The entity files have been created in dir '{self.nlu_folder_path}'."
        )

    def _handle_entities(self) -> tuple:
        synonym_content, lookup_content, compound_content = {}, {}, {}

        for entity_file in self.entities_path.glob(f"*_entries_{self.language}.json"):
            entity_name = camel_to_snake(entity_file.stem).replace(
                f"_entries_{self.language}", ""
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
                            self._init_compound_file_content()
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
                    synonyms_file_path = self.nlu_folder_path / f"{self.agent_name}.yml"
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
                        self._handle_lookup(entry),
                    )

        return synonym_content, lookup_content, compound_content

    def _update_content(self, content_dict: dict, file_path: Path, new_content: str):
        if file_path not in content_dict:
            content_dict[file_path] = ""
        content_dict[file_path] += new_content

    def _handle_synonyms(self, entry: dict) -> str:
        """Returns Rasa format string for Dialogflow synonyms."""
        synonym = entry["value"]
        examples = "\n".join(f"    - {syn}" for syn in entry["synonyms"])
        return f"- synonym: {synonym}\n  examples: |\n{examples}\n\n"

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
