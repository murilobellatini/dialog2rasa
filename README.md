# Dialog2Rasa Converter

Easily convert Dialogflow agents to Rasa format for Rasa version 3+. This tool automates the migration to Rasa, converting Dialogflow exports into Rasa YAML format.

## Installation

Install `dialog2rasa` with:

```bash
pip install dialog2rasa
```

For more details, visit [PyPI](https://pypi.org/project/dialog2rasa/).

## Usage

Unzip your Dialogflow export first. Then, convert it to Rasa format with:

```sh
dialog2rasa -p path/to/extracted/dialogflow/export -l language_code
```

### Command Details

- `-p PATH`: Path to the Dialogflow export’s extracted folder.
- `-l LANGUAGE`: Language code (e.g., 'en' for English), defaults to 'de' (German).

The conversion output is saved in `/output/[LANGUAGE_CODE]` within the Dialogflow agent’s directory, with `[LANGUAGE_CODE]` being the actual language code used.

## Features and Limitations

- **Features**: Converts intents, entities, and utterances to Rasa YAML.
- **Limitations**:
  - Does not support compound entities directly; creates pseudo-yaml `__compound_` with prefix as workaround.
  - Groups entities with a single synonym in a lookup table; handles entities multiple synonyms also as synonyms in Rasa.
  - Names output NLU data after the agent for easy project integration.

> Note: See `test/mockup-agent` and its reference output [here](./tests/mockup-agent) to understand these limitations.

## Contributing

Your feedback and contributions are appreciated to enhance this tool. Report bugs or suggest features via issues or pull requests.

### Testing

The package includes automated tests. Contribute by writing tests with `pytest` for your code changes to maintain functionality and reliability.

## License

Licensed under the Apache 2.0 License.
