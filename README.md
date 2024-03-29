# Dialog2Rasa Converter

Transform your Dialogflow agents into Rasa format, suitable for Rasa version 3 and above. This CLI tool streamlines the migration process from Dialogflow to Rasa, ensuring a smoother transition for chatbot migrations. It converts the Dialogflow export into Rasa YAML format.

## Installation

To install `dialog2rasa`, simply run:

```bash
pip install dialog2rasa
```

For more information and details about the package, you can visit the PyPI page at: <https://pypi.org/project/dialog2rasa/>.

## Usage

After installation, convert your Dialogflow extracted export (i.e. unzip it first) to Rasa format using the command:

```sh
dialog2rasa -p path/to/extracted/dialogflow/export -l language_code
```

More specifically:

```bash
usage: dialog2rasa [-h] --path PATH [--language LANGUAGE]

Transforms a Dialogflow agent into Rasa format. The result is saved in /output/[LANGUAGE_CODE], where [LANGUAGE_CODE] is replaced with the actual language code (e.g., 'en', 'de'), inside the Dialogflow agent's directory.

options:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  Path to the Dialogflow agent's extracted/unzipped folder.
  --language LANGUAGE, -l LANGUAGE
                        Language code (e.g., 'en' for English) of the Dialogflow agent. Defaults to 'de' (German).
```

## Features and Limitations

- Converts Dialogflow intents, entities, and utterances to Rasa-compatible YAML format.
- **Limitations**:
  - **Compound Entities**: Does not handle compound entities directly. Instead, creates pseudo YAML files with a `__compound__` prefix.
  - **Synonym Entities**: Groups single synonym entities within a lookup table. Entities with multiple synonyms are handled accordingly.
  - **Output Naming**: The output NLU data is named after the agent, facilitating integration into larger projects (assuming `nlu` as a directory).

## Contributing

Feedback and contributions are welcome as we work towards making this tool more robust and versatile. For bugs, feature requests, or contributions, please open an issue or pull request.

### Testing

This project includes automated unit tests when distributed as a PyPi package (triggered by Github actions workflow). Please be sure to test your code and extend the tests with `pytest` before submitting a pull request. This will ensure reliability and functionality of the package.

## License

This project is licensed under the Apache 2.0 License.
