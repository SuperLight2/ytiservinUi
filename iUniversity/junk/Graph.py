__author__ = 'gumerovif'

from IDGenerator.IDGenerator import IDGenerator
from datetime import datetime


class VertexDescriptor:
    def __init__(self, name, description):
        self.uid = IDGenerator.generate_unique_id()
        self.name = name
        self.description = description


class EdgeDirection(object):
    UNDIRECTED = 1
    DIRECTED = 2
    ASYMMETRICAL = 3


class EdgeDescriptor:
    def __init__(self, name, descrition, first_object_type, second_object_type, edge_direction, asymmetrical_edge_type):
        self.uid = IDGenerator.generate_unique_id()
        self.name = name
        self.description = descrition
        self.first_object_type = first_object_type
        self.second_object_type = second_object_type
        self.edge_direction = edge_direction
        self.asymmetrical_edge_type = asymmetrical_edge_type


class Vertex:
    def __init__(self, vertex_type_id):
        self.uid = IDGenerator.generate_unique_id()
        self.vertex_type_id = vertex_type_id
        self.mod_timestamps = [datetime.now()]


class Edge:
    def __init__(self, edge_type_id, first_vertex_uid, second_vertex_uid):
        self.uid = IDGenerator.generate_unique_id()
        self.edge_type_id = edge_type_id
        self.first_vertex_uid = first_vertex_uid
        self.second_vertex_uid = second_vertex_uid

class Graph(object):
    pass