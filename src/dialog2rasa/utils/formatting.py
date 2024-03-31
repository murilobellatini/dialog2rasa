# Entity formatting utils


def initialize_compound_file_header() -> str:
    """Returns the initial content for a new compound entity file."""
    header_content = "# Compound entity: Manual adaptation needed for Rasa\n"
    header_content += 'version: "3.1"\n\nnlu:\n'
    return header_content


def format_synonyms_for_rasa(entry: dict) -> str:
    """Returns Rasa format string for Dialogflow synonyms."""
    synonym = entry["value"]
    examples = "\n".join(f"      - {syn}" for syn in entry["synonyms"])
    return f"  - synonym: {synonym}\n    examples: |\n{examples}\n\n"


def format_lookup_for_rasa(entry: dict) -> str:
    """Returns Rasa format string for Dialogflow lookup tables."""
    return "\n".join(entry["synonyms"]) + "\n"


def format_compounds_for_rasa(entry: dict) -> str:
    """
    Returns Rasa format string for pseudo-compound entities from Dialogflow.
    No need to check for new files here, handled in convert method.
    """
    synonym = entry["value"]
    examples = "\n".join(f"      - {syn}" for syn in entry["synonyms"])
    return f"  - synonym: {synonym}\n    examples: |\n{examples}\n\n"
