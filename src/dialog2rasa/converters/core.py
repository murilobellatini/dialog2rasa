from pathlib import Path
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
        agent_name = agent_dir.name.replace("Agent-", "").replace("-", "_").lower()
        super().__init__(agent_dir, agent_name, language, output_file, "nlu")
        """Initializes converter settings."""

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
