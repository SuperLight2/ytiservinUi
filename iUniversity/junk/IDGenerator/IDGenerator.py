__author__ = 'gumerovif'

import random

class IDGenerator(object):
    IDs = set()

    @classmethod
    def check_existance(cls, id):
        return id in IDGenerator.IDs

    @classmethod
    def add_id(cls, id):
        IDGenerator.IDs.add(id)

    @classmethod
    def generate_unique_id(cls):
        while True:
            id = random.randint(0, 1e18)
            if not IDGenerator.check_existance(id):
                IDGenerator.add_id(id)
                return id

if __name__ == '__main__':
    for i in xrange(5):
        id = IDGenerator.generate_unique_id()
        print id
    print IDGenerator.IDs