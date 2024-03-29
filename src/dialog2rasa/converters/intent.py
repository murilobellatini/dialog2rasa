from pathlib import Path
from typing import Optional

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import camel_to_snake, logger
from dialog2rasa.utils.io import read_json_file, write_to_file


class IntentConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        agent_name: str,
        language: str,
        output_file: Optional[str] = None,
    ) -> None:
        super().__init__(agent_dir, agent_name, language, output_file, "nlu")
        self.intents_path = agent_dir / "intents"

    def convert(self) -> None:
        """Converts Dialogflow intents to Rasa NLU format."""
        converted_intents = self._handle_intents()
        write_to_file(self.output_path, converted_intents)
        logger.debug(f"The file '{self.output_path}' has been created.")

    def _handle_intents(self) -> str:
        """Handles conversion of individual Dialogflow intents."""
        converted_intents = 'version: "3.1"\n\nnlu:\n'
        intent_file_stem = f"_usersays_{self.language}"

        for file in sorted(self.intents_path.glob(f"*{intent_file_stem}.json")):
            intent_name = camel_to_snake(file.stem.split(intent_file_stem)[0])
            data = read_json_file(file)
            examples = self._handle_examples(data)
            converted_intents += (
                f"  - intent: {intent_name}\n    examples: |\n{examples}\n"
            )

        return converted_intents

    def _handle_examples(self, data: dict) -> str:
        """Handles conversion of Dialogflow examples to Rasa format."""
        examples = ""
        for d in data:
            text = "".join(
                (
                    f'[{fragment["text"]}]'
                    f'({fragment["meta"].replace("@", "").replace(".", "_")})'
                    if "meta" in fragment
                    else fragment["text"]
                )
                for fragment in d["data"]
            )
            examples += f"      - {text.strip()}\n"
        return examples
