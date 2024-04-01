import logging
import sys
from pathlib import Path

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.converters.manager import get_converter
from dialog2rasa.utils.io import reset_directory


class DialogflowToRasaConverter(BaseConverter):
    """Converts Dialogflow agent files (.zip export) to Rasa format."""

    def __init__(self, agent_dir: Path, language: str, logger: logging.Logger) -> None:
        """Initializes converter settings."""
        super().__init__(agent_dir, language, logger)
        if not self._language_files_exist:
            self.logger.error(
                f"Language code '{self.language}' files not found "
                "in intents or entities directories. Please check if "
                "the language was correctly input."
            )
            sys.exit(1)

    @property
    def _language_files_exist(self) -> bool:
        """Checks if language-specific files exist in the agent directories."""
        language_files_exist = any(
            file.name.endswith(f"_{self.language}.json")
            for file in self.intents_dir.glob("*.json")
        ) and any(
            file.name.endswith(f"_entries_{self.language}.json")
            for file in self.entities_dir.glob("*.json")
        )
        return language_files_exist

    def _initialize_converters(self) -> None:
        """Initializes all required converters."""
        converter_types = ["intent", "utterance", "entity", "slot"]
        self.converters: dict[str, BaseConverter] = {}
        for converter_type in converter_types:
            self.converters[converter_type] = get_converter(
                converter_type, self.agent_dir, self.language, self.logger
            )

    def convert_all(self) -> None:
        """Converts all Dialogflow files to Rasa format."""
        self.logger.debug("Starting conversion...")

        self.logger.warning(f"Clearing all contents from '{self.output_dir}'...")
        reset_directory(self.output_dir, "data/nlu/lookup")
        self.logger.debug("Output directory cleared.")

        self._initialize_converters()

        for _, converter in self.converters.items():
            converter.convert()

        self.logger.info(
            "Conversion completed. "
            f"The output files can be found in '{self.output_dir}'."
        )
