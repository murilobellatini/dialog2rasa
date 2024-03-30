# Dialog2Rasa Converter

[![Build Status](https://github.com/murilobellatini/dialog2rasa/actions/workflows/python-publish.yml/badge.svg)](https://github.com/murilobellatini/dialog2rasa/actions)
[![PyPI version](https://badge.fury.io/py/dialog2rasa.svg)](https://pypi.org/project/dialog2rasa/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dialog2rasa.svg)](https://pypi.org/project/dialog2rasa/)
[![License](https://img.shields.io/pypi/l/dialog2rasa.svg)](https://github.com/murilobellatini/dialog2rasa/blob/main/LICENSE)

## About dialog2rasa

Easily convert Dialogflow agents to Rasa format for Rasa version 3+. This tool automates the migration to Rasa, converting Dialogflow exports into Rasa YAML format.

### Installation

Install `dialog2rasa` with:

```bash
pip install dialog2rasa
```

For more details, visit [PyPI](https://pypi.org/project/dialog2rasa/).

### Usage

Unzip your Dialogflow export first. Then, convert it to Rasa format with:

```sh
dialog2rasa -p path/to/extracted/dialogflow/export -l language_code
```

#### Command Details

- `-p PATH`: Path to the Dialogflow export’s extracted folder.
- `-l LANGUAGE`: Language code (e.g., 'en' for English), defaults to 'de' (German).

The conversion output is saved in `/output/[LANGUAGE_CODE]` within the Dialogflow agent’s directory, with `[LANGUAGE_CODE]` being the actual language code used.

### Features and Limitations

- **Features**: Converts intents, entities, and utterances to Rasa YAML.
- **Limitations**:
  - As Rasa doesn't natively support compound entities, this converter introduces a workaround by generating a pseudo-YAML file, prefixed with `__compound_`, which allows users to define their handling strategy.
  - It consolidates entities that share a single synonym into a lookup table, while also treating entities with multiple synonyms as synonyms within Rasa.
  - The output NLU YAML file is named after the agent, facilitating project integration by placing it within an `nlu` folder.

> Note: See `test/mockup-agent` and its reference output [here](./tests/mockup-agent) to understand these limitations.

### Contributing

Your feedback and contributions are appreciated to enhance this tool. Report bugs or suggest features via issues or pull requests.

#### Testing

The package includes automated tests (see `.github/workflows/python-publish.yml` [here](.github/workflows/python-publish.yml)) in a Continuous Integration workflow with PyPi. Contribute by writing tests with `pytest` for your code changes to maintain functionality and reliability.

### License

Licensed under the Apache 2.0 License.
