# Dialog2Rasa Converter

[![Build Status](https://github.com/murilobellatini/dialog2rasa/actions/workflows/python-publish.yml/badge.svg)](https://github.com/murilobellatini/dialog2rasa/actions)
[![PyPI version](https://badge.fury.io/py/dialog2rasa.svg)](https://pypi.org/project/dialog2rasa/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dialog2rasa.svg)](https://pypi.org/project/dialog2rasa/)
[![License](https://img.shields.io/pypi/l/dialog2rasa.svg)](https://github.com/murilobellatini/dialog2rasa/blob/main/LICENSE)

Convert Dialogflow agents to Rasa format easily. Supports Rasa 3+.

For a detailed architecture flow, see the [Conversion Process Diagram](https://github.com/murilobellatini/dialog2rasa/blob/main/docs/conversion-process-diagram.md).

## Installation

Install `dialog2rasa` with:

```bash
pip install dialog2rasa
```

For more details, visit [PyPI](https://pypi.org/project/dialog2rasa/).

## Usage

Export your Dialogflow agent (details [here](https://cloud.google.com/dialogflow/es/docs/agents-settings#export)), unzip it, and then, convert it to Rasa format with:

```sh
dialog2rasa -p path/to/extracted/dialogflow/export -l language_code -v
```

### Command Details

- `-p PATH`: Path to the Dialogflow export’s extracted folder.
- `-l LANGUAGE` (optional): Language code (e.g., 'en' for English), defaults to 'de' (German).
- `-v VERBOSE` (optional): Increase output verbosity for debugging purposes, defaults to 'False'.

The conversion output is saved in `/output/[LANGUAGE_CODE]` within the Dialogflow agent’s directory, with `[LANGUAGE_CODE]` being the actual language code used.

#### Output File Format

For detailed insights into how the output data is structured, visit our documentation [here](https://github.com/murilobellatini/dialog2rasa/blob/main/docs/file-generation-process.md).

### Features and Limitations

Converts intents, entities, and utterances to Rasa YAML.

### Limitations

- **Compound Entity Conversion**: Generates `__compound_` prefixed pseudo-YAML for Rasa's unsupported compound entities, allowing for custom handling by the user.

- **Entity Conversion Strategy:** Our approach involves two distinct methods based on the number of synonyms associated with each reference value.
  - **Single Synonym Entities:** Dialogflow entities that have reference values with only one synonym each are consolidated into a Rasa lookup table. This table is named after the original Dialogflow entity. This method facilitates efficient entity recognition in Rasa for these cases, since it usually indicates a Dialogflow design choice of accumulating synonyms as reference value, which which can increase very quickly. Hence, should be more easily manageable and readable via lookup tables.
  - **Multiple Synonyms Entities:** For Dialogflow entities where reference values have multiple synonyms, we create a corresponding Rasa entity. In these instances, extra synonyms are grouped under their respective reference value to maintain the nuanced relationships between them. Typically, the number of synonyms is smaller here, making it easier to digest and maintain within the nlu.yml under the synonym key.

This approach comes from what we've seen work in practice, showing that Rasa tends to do a better job of capturing entities this way. However, we're completely open to the idea that there may be other, possibly better ways to do this in certain cases. If you have any ideas or suggestions on how to tweak or improve this part, we'd love to hear them!

> **Note**: See the Output File Format [here](#output-file-format) to understand these limitations.

### Contributing

Your feedback and contributions are appreciated to enhance this tool. Report bugs or suggest features via issues or pull requests.

#### Testing

The package includes automated tests that are run in two Continuous Integration workflows:

- **PR Validation CI**: Tests are run on pull requests to ensure code quality and functionality before merging (more details [here](https://github.com/murilobellatini/dialog2rasa/blob/main/.github/workflows/pr-validation-ci.yml)).
- **Python Publish**: Upon merging, tests are run again before deployment to PyPI (more details [here](https://github.com/murilobellatini/dialog2rasa/blob/main/.github/workflows/python-publish.yml)).

Please contribute by writing tests with `pytest` for your code changes to maintain functionality and reliability.

### License

Licensed under the Apache 2.0 License.
