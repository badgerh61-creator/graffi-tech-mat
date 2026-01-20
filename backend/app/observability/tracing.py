import uuid
from contextlib import contextmanager

class Span:
    def __init__(self, name):
        self.name = name
        self.trace_id = uuid.uuid4().hex

@contextmanager
def start_span(name):
    span = Span(name)
    try:
        yield span
    finally:
        pass

