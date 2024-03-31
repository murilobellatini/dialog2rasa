from dialog2rasa.converters.base import BaseConverter
from dialog2rasa.converters.entity import EntityConverter
from dialog2rasa.converters.entity_slot import EntitySlotConverter
from dialog2rasa.converters.intent import IntentConverter
from dialog2rasa.converters.utterance import UtteranceConverter


def get_converter(type_: str, *args, **kwargs) -> BaseConverter:
    converters = {
        "intent": IntentConverter,
        "utterance": UtteranceConverter,
        "entity": EntityConverter,
        "entity_slot": EntitySlotConverter,
    }
    return converters[type_](*args, **kwargs)
