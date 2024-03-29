from abc import abstractmethod
from pathlib import Path
from typing import Optional


class BaseConverter:
    """
    Base converter to simplify initialization. Main function are:
    1) Manipulate the strings from Dialogflow export files and;
    2) Export the output files following the RASA YAML-format.
    """

    def __init__(
        self,
        agent_dir: Path,
        agent_name: str,
        languages: tuple,
        output_file: Optional[str] = None,
        sub_dir: str = "",
    ) -> None:
        self.agent_dir = agent_dir
        self.agent_name = agent_name
        self.languages = languages
        self.base_output_path = agent_dir / "output"
        self.nlu_folder_path = (
            self.base_output_path / "data" / "nlu"
            if sub_dir == "nlu"
            else self.base_output_path
        )
        self.output_file = output_file if output_file else f"{self.agent_name}.yml"
        self.output_path = self.nlu_folder_path / self.output_file

    @abstractmethod
    def convert(self) -> None: ...
