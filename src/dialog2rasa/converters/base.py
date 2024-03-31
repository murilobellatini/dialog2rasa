from abc import abstractmethod
from pathlib import Path


class BaseConverter:
    """
    Base converter to simplify initialization. Main functions are:
    1) Manipulate the strings from Dialogflow export files and;
    2) Export the output files following the RASA YAML-format.
    """

    def __init__(
        self,
        agent_dir: Path,
        language: str,
    ) -> None:
        self.agent_dir = agent_dir
        self.language = language
        self.initialize_paths()

    def initialize_paths(self) -> None:
        self.output_dir = self.agent_dir / "output" / self.language
        self.domain_file_path = self.output_dir / "domain.yml"
        self.nlu_folder_dir = self.output_dir / "data" / "nlu"
        self.nlu_output_path = self.nlu_folder_dir / "nlu.yml"
        self.lookup_dir = self.nlu_folder_dir / "lookup"
        self.intents_dir = self.agent_dir / "intents"
        self.entities_dir = self.agent_dir / "entities"

    @abstractmethod
    def convert(self) -> None:
        pass
