## Conversion Process Overview

The following diagram illustrates the process flow for converting Dialogflow JSON into Rasa YAML format using the `DialogflowToRasaConverter` tool. Each converter component (`IntentConverter`, `EntityConverter`, `UtteranceConverter`) is responsible for translating a specific part of the Dialogflow structure into the corresponding Rasa format, which is then merged to create the final Rasa-compatible YAML output.

```mermaid
graph TD
    A[Dialogflow JSON Input] -->|Read by| B(DialogflowToRasaConverter)
    B --> |Delegates conversion to| C(IntentConverter)
    B --> |Delegates conversion to| D(EntityConverter)
    B --> |Delegates conversion to| E(UtteranceConverter)
    
    C --> |Generates| F{Intents in <br>nlu/mockup-agent.yml}
    D --> |Generates| G{"Synonyms, Lookup<br>& Compounds in nlu/"}
    E --> |Generates| H{Utterances in domain.yml}
    
    F -.-> |Merged into| I[Final Rasa YAML Output]
    G -.-> |Merged into| I
    H -.-> |Merged into| I

```
