"""
opysnippets/int_id_generator:1.0.0
"""
import sys


class IntIDGenerator:
    def __init__(self, to_string=True):
        self._last_id = -1
        self._to_string = to_string

    def __call__(self):
        if self._last_id >= sys.maxsize:
            self._last_id = -1
        self._last_id += 1
        return str(self._last_id) if self._to_string else self._last_id
