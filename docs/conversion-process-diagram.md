## Conversion Process Overview

The following diagram illustrates the process flow for converting Dialogflow JSON into Rasa YAML format using the `DialogflowToRasaConverter` tool. Each converter component (`IntentConverter`, `EntityConverter`, `UtteranceConverter`) is responsible for translating a specific part of the Dialogflow structure into the corresponding Rasa format, which is then merged to create the final Rasa-compatible YAML output.

```mermaid
graph TD
    A[Dialogflow JSON Input] -->|Read by| B(DialogflowToRasaConverter)
    B --> |Delegates conversion to| C(IntentConverter)
    B --> |Delegates conversion to| D(EntityConverter)
    B --> |Delegates conversion to| E(UtteranceConverter)
    
    C --> |Generates| F{Rasa Intents YAML}
    D --> |Generates| G{Rasa Entities YAML}
    E --> |Generates| H{Rasa Utterances YAML}
    
    F -.-> |Merged into| I[Final Rasa YAML Output]
    G -.-> |Merged into| I
    H -.-> |Merged into| I

```
