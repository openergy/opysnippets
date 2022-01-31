"""
opysnippets/progress:1.0.0
"""
import contextlib
import sys


class ProgressStreamer:
    def __init__(self, progress_fct):
        self.progress_fct = progress_fct

    def write(self, value):
        if value == "\n":
            value = None  # print() => updates beat without line returns
        self.progress_fct(progress_message=value)

    def flush(self):
        pass


@contextlib.contextmanager
def stdout_as_progress(progress_fct):
    """
    Parameters
    ----------
    progress_fct: (progress_message=None, progress_value=None)
    """
    _stdout = sys.stdout
    streamer = ProgressStreamer(progress_fct)
    try:
        sys.stdout = streamer
        yield
    finally:
        sys.stdout = _stdout
