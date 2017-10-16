from models.base_model import BaseModel
from models.midi_changer import MidiHueController

__all__ = [
    "BaseModel",
]


def make_model(config):
    if config['agent_name'] in __all__:
        return globals()[config['model_name']](config)
    else:
        raise Exception('The model name %s does not exist' % config['model_name'])


def get_model_class(config):
    if config['model_name'] in __all__:
        return globals()[config['model_name']]
    else:
        raise Exception('The model name %s does not exist' % config['model_name'])
