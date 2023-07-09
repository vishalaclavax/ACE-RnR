from copy import deepcopy
from app import cosmos


class Entity(object):
    """Base entity for cosmos document"""
    def __init__(self, name):
        self.name = name
        self.fields = {}

    def check_entity_field(self, entity_dict):
        return entity_dict.get(cosmos.entity_field) == self.name

    def __call__(self, *args, **kwargs):
        data = deepcopy(self.fields)
        if len(args) and isinstance(args[0], dict):
            data.update(args[0])
        else:
            data.update(kwargs)
        data[cosmos.entity_field] = self.name
        return data
