__author__ = 'gumerovif'

from id_generator import IDGenerator
from datetime import datetime


class Resource:
    def __init__(self):
        self.id = IDGenerator.generate_unique_id()
        self.mod_timestamps = [datetime.now()]

    def get_id(self):
        return self.id
