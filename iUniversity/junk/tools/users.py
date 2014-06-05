__author__ = 'gumerovif'

from core.id_generator import IDGenerator

class User:
    def __init__(self, first_name, last_name):
        self.id = IDGenerator.generate_unique_id()
        self.first_name = first_name
        self.last_name = last_name
        self.in_groups = set()
