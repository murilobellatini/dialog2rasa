import argparse
from pathlib import Path

from common.converters import get_converter
from common.io import reset_directory
from common.loggers import logger


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
        self.intent_converter = get_converter(
            "intent", self.agent_dir, self.agent_name, self.languages
        )
        self.utterance_converter = get_converter(
            "utterance", self.agent_dir, self.agent_name, self.languages
        )
        self.entity_converter = get_converter(
            "entity", self.agent_dir, self.agent_name, self.languages
        )

    def convert_all(self) -> None:
        """Converts all Dialogflow files to Rasa format."""
        logger.info("Starting conversion...")
        reset_directory(self.output_dir, "data/nlu/lookup")

        self._initialize_converters()

        self.intent_converter.convert()
        self.utterance_converter.convert()
        self.entity_converter.convert()

        logger.info(
            "Conversion completed. "
            f"The output files can be found in '{self.output_dir}'"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Dialogflow agent to Rasa format."
    )
    parser.add_argument(
        "agent_path",
        nargs="?",
        help="The path to the extracted Dialogflow agent directory",
    )

    args = parser.parse_args()

    converter = DialogflowToRasaConverter(args.agent_path)
    converter.convert_all()
