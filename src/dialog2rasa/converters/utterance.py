from pathlib import Path
from typing import Optional

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_to_file


class UtteranceConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        agent_name: str,
        language: str,
        output_file: Optional[str] = "domain.yml",
    ) -> None:
        super().__init__(agent_dir, agent_name, language, output_file)

    def convert(self) -> None:
        """Converts Dialogflow utterances to Rasa domain format."""
        responses_folder_path = self.agent_dir / "intents"
        converted_responses = self._handle_responses(responses_folder_path)
        write_to_file(self.output_path, converted_responses)
        logger.info(f"The file '{self.output_path}' has been created.")

    def _handle_responses(self, responses_folder_path: Path) -> str:
        """Handles conversion of Dialogflow responses to Rasa format."""
        converted_responses = "responses:\n"
        for file in sorted(responses_folder_path.iterdir()):
            if not file.name.endswith(f"usersays_{self.language}.json"):
                intent_name = camel_to_snake(file.stem)
                data = read_json_file(file)
                for response in data.get("responses", []):
                    converted_responses += self._handle_utter_message(
                        intent_name, response
                    )
        return converted_responses

    def _handle_utter_message(self, intent_name: str, response: dict) -> str:
        """Handles conversion of individual Dialogflow utter messages."""
        converted_utter = ""
        for message in response.get("messages", []):
            if message.get("lang") == self.language:
                if "speech" in message:
                    converted_utter += f"  utter_{intent_name}:\n"
                    for s in message["speech"]:
                        converted_utter += f'    - text: "{s}"\n'
                    converted_utter += "\n"
        return converted_utter
