from pathlib import Path

from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.utils.general import logger
from dialog2rasa.utils.io import write_to_file


class SlotConverter(BaseConverter):
    def __init__(
        self,
        agent_dir: Path,
        language: str,
    ) -> None:
        super().__init__(agent_dir, language)

    def convert(self) -> None:
        """Appends Dialogflow entities as slots to domain.yaml."""
        slot_entities_content = self._gather_slot_data()
        if slot_entities_content:
            write_to_file(self.domain_file_path, slot_entities_content, "a")
            logger.warning(
                "Entities have been added as slots to the domain file. "
                "Please review slot types and mappings."
            )

    def _gather_slot_data(self) -> str:
        """Returns entities as slots for appending to the Rasa domain file."""
        if not self.domain_file_path.exists():
            logger.error(f"Domain file {self.domain_file_path} not found.")
            return ""

        entity_names = sorted(
            set(
                [
                    x.stem.split("_entries")[0]
                    for x in self.entities_dir.glob(f"*_entries_{self.language}.json")
                ]
            )
        )
        entities_str = "\n  - ".join(entity_names)
        slots_str = "\n".join(
            f"  {entity_name}:\n    type: text\n    "
            "influence_conversation: false\n    mappings:\n    "
            f"- type: from_entity\n      entity: {entity_name}\n"
            for entity_name in entity_names
        )

        return (
            "# TODO: Review assumption of Dialogflow "
            "entities as slots and entities. "
            "Confirm the types and mappings.\nentities:"
            f"\n  - {entities_str}\n\nslots:\n{slots_str}\n"
        )
