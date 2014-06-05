__author__ = 'gumerovif'

from core.id_generator import IDGenerator
from u_query import UQuery


class UGraphStorage(object):
    _storage = dict()

    @classmethod
    def run(cls, uqeury):
        if isinstance(uqeury, UQuery):
            raise BaseException("Can't run non-UQuery type queries")

    # we should use this function when creating a new objects
    @classmethod
    def generate_new_id(cls, u_type):
        pass

    @classmethod
    def load_from_db(cls, db_name):
        pass