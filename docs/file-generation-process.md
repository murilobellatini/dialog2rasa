# File Structure and Generation

This section outlines the structure of test data and the file generation process for converting Dialogflow data to Rasa format.

## Structure Overview

See the actual files of our `mockup-agent` for more details [here](tests/mockup-agent).

``` bash
/tests/mockup-agent
├── entities # Dialogflow entity definitions
│   ├── full_name_entries_en.json
│   ├── full_name.json
│   ├── yes_entries_en.json
│   └── yes.json
├── intents  # Dialogflow intent definitions
│   ├── chitchat.start.json
│   ├── chitchat.start_usersays_en.json
│   ├── default.cancel.json
│   └── default.cancel_usersays_en.json
└── reference_output # Rasa output post-conversion
    └── en # English language output
        ├── data
        │   └── nlu # Natural Language Understanding data
        │       ├── __compound__full_name.yml  # Compound entities workaround for user review
        │       ├── lookup # Lookup tables (synonyms with only one value under an entity)
        │       │   └── yes.txt
        │       └── mockup-agent.yml  # Merged NLU with intents and other synonyms
        └── domain.yml  # Rasa domain with utterances and synonyms
```
