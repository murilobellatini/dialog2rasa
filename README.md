# Dialog2Rasa Converter

Transform your Dialogflow agents into Rasa format, suitable for Rasa version 3 and above. This CLI tool streamlines the migration process from Dialogflow to Rasa, ensuring a smoother transition for developers aiming to leverage Rasa's capabilities.

## Installation

The package is in the process of being made available as a Python package. Installation instructions will be provided upon release.

## Usage

After installation, convert your Dialogflow export to Rasa format using the command:

```sh
dialog2rasa -p path/to/extracted/dialogflow/export
```

## Features and Limitations

- Converts Dialogflow intents, entities, and utterances to Rasa-compatible YAML format.
- **Limitations**:
  - **Compound Entities**: Does not handle compound entities directly. Instead, creates pseudo YAML files with a `__compound__` prefix.
  - **Synonym Entities**: Groups single synonym entities within a lookup table. Entities with multiple synonyms are handled accordingly.
  - **Output Naming**: The output NLU data is named after the agent, facilitating integration into larger projects (assuming `nlu` as a directory).

## Contributing

Feedback and contributions are welcome as we work towards making this tool more robust and versatile. For bugs, feature requests, or contributions, please open an issue or pull request.

## License

This project is licensed under the Apache 2.0 License.
