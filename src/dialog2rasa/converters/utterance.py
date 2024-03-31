from pathlib import Path

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_to_file


class UtteranceConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        language: str,
    ) -> None:
        super().__init__(agent_dir, language)

    def convert(self) -> None:
        """Converts Dialogflow utterances to Rasa domain format."""
        responses_folder_path = self.agent_dir / "intents"
        converted_responses = self._gather_response_data(responses_folder_path)
        write_to_file(self.domain_file_path, converted_responses)
        logger.debug(f"The file '{self.domain_file_path}' has been created.")

    def _gather_response_data(self, responses_folder_path: Path) -> str:
        """Gathers response data and converts it into Rasa format."""
        converted_responses = "responses:\n"
        for file in sorted(responses_folder_path.iterdir()):
            if not file.name.endswith(f"usersays_{self.language}.json"):
                intent_name = camel_to_snake(file.stem)
                data = read_json_file(file)
                for response in data.get("responses", []):
                    converted_responses += self._gather_utterance_data(
                        intent_name, response
                    )
        return converted_responses

    def _gather_utterance_data(self, intent_name: str, response: dict) -> str:
        """Gathers utterance data and converts it into Rasa format."""
        converted_utter = ""
        for message in response.get("messages", []):
            if message.get("lang") == self.language:
                if "speech" in message:
                    converted_utter += f"  utter_{intent_name}:\n"
                    for s in message["speech"]:
                        converted_utter += f'    - text: "{s}"\n'
                    converted_utter += "\n"
        return converted_utter
