from pathlib import Path
import sys
from typing import Optional

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.converters.manager import get_converter
from dialog2rasa.utils.general import logger
from dialog2rasa.utils.io import reset_directory


class DialogflowToRasaConverter(BaseConverter):
    """Converts Dialogflow agent files (.zip export) to Rasa format."""

    def __init__(
        self,
        agent_dir: Path,
        language: str,
        output_file: Optional[str] = None,
    ) -> None:
        """Initializes converter settings."""
        super().__init__(agent_dir, agent_dir.stem, language, output_file, "nlu")
        if not self._check_language_files_existence():
            logger.error(
                f"Language code '{self.language}' files not found "
                "in intents or entities directories. Please check if "
                "the language was correctly input"
            )
            sys.exit(1)

    def _check_language_files_existence(self) -> bool:
        """Checks if language-specific files exist in the agent directories."""
        intents_path = self.agent_dir / "intents"
        entities_path = self.agent_dir / "entities"
        language_files_exist = any(
            file.name.endswith(f"_{self.language}.json")
            for file in intents_path.glob("*.json")
        ) and any(
            file.name.endswith(f"_entries_{self.language}.json")
            for file in entities_path.glob("*.json")
        )
        return language_files_exist

    def _initialize_converters(self) -> None:
        """Initializes all required converters."""
        converter_types = ["intent", "utterance", "entity"]
        self.converters: dict[str, BaseConverter] = {}
        for converter_type in converter_types:
            self.converters[converter_type] = get_converter(
                converter_type, self.agent_dir, self.agent_name, self.language
            )

    def convert_all(self) -> None:
        """Converts all Dialogflow files to Rasa format."""
        logger.info("Starting conversion...")
        reset_directory(self.output_dir, "data/nlu/lookup")

        self._initialize_converters()

        for _, converter in self.converters.items():
            converter.convert()

        logger.info(
            "Conversion completed. "
            f"The output files can be found in '{self.output_dir}'"
        )
