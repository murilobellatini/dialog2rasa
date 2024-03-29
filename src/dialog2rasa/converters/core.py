from pathlib import Path

from src.dialog2rasa.converters.base import BaseConverter
from src.dialog2rasa.converters.manager import get_converter
from src.dialog2rasa.utils.io import reset_directory
from src.dialog2rasa.utils.general import logger


class DialogflowToRasaConverter:
    """Converts Dialogflow agent files (.zip export) to Rasa format."""

    def __init__(self, agent_dir: str, languages=("de",)) -> None:
        """Initializes converter settings."""
        self.agent_dir = Path(agent_dir)
        self.languages = languages
        self.agent_name = (
            self.agent_dir.name.replace("Agent-", "").replace("-", "_").lower()
        )
        self.output_dir = self.agent_dir / "output"
        self.lookup_path = self.output_dir / "data" / "nlu" / "lookup"

    def _initialize_converters(self):
        """Initializes all required converters."""
        converter_types = ["intent", "utterance", "entity"]
        self.converters: dict[str, BaseConverter] = {}
        for converter_type in converter_types:
            self.converters[converter_type] = get_converter(
                converter_type, self.agent_dir, self.agent_name, self.languages
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
