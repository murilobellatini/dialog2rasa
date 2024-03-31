from abc import abstractmethod
from pathlib import Path
from typing import Optional


class BaseConverter:
    """
    Base converter to simplify initialization. Main functions are:
    1) Manipulate the strings from Dialogflow export files and;
    2) Export the output files following the RASA YAML-format.
    """

    def __init__(
        self,
        agent_dir: Path,
        agent_name: str,
        language: str,
        output_file: Optional[str] = None,
        sub_dir: str = "",
    ) -> None:
        self.agent_dir = agent_dir
        self.agent_name = agent_name
        self.language = language
        self.initialize_paths(output_file, sub_dir)

    def initialize_paths(self, output_file: Optional[str], sub_dir: str) -> None:
        self.output_dir = self.agent_dir / "output" / self.language
        self.nlu_folder_path = (
            self.output_dir / "data" / "nlu" if sub_dir == "nlu" else self.output_dir
        )
        self.output_file = output_file if output_file else f"{self.agent_name}.yml"
        self.output_path = self.nlu_folder_path / self.output_file
        self.lookup_path = self.nlu_folder_path / "lookup"
        self.intents_path = self.agent_dir / "intents"
        self.entities_path = self.agent_dir / "entities"
        self.domain_file_path = self.output_dir / "domain.yml"

    @abstractmethod
    def convert(self) -> None: ...
