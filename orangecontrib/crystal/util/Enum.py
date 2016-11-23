"""
---OK---
"""


class Enum(object):
    def __init__(self, enum_type):
        self.enum_type = enum_type

    def __eq__(self, candidate):
        return self.enum_type == candidate.enum_type

    def __ne__(self, candidate):
        return not (self == candidate)
