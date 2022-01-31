"""
opysnippets/living_source:1.0.0
"""
import textwrap
import traceback
import re


class SourceLoadError(Exception):
    pass


class SourceRunError(Exception):
    pass


class SourceVarDoesNotExistError(Exception):
    pass


class MultipleSourceVarReturnedError(Exception):
    pass


def traceback_wrapper(f):
    if not callable(f):
        return f

    def _f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # todo: make intelligible traceback
            tr = traceback.format_exc()
            tr = re.sub(
                """File "<string>", line (\d+),""",
                lambda m: """File "<string>", line %s,""" % (int(m.group(1)) - 1),
                tr)
            raise SourceRunError(
                "Error while executing source code:\n%s" % textwrap.indent(tr, "  | ")) from None
    return _f


class LivingSource:
    def __init__(self, source):
        # run source
        try:
            exec("""def main():
%s
    return locals()
""" % textwrap.indent(source, "    "))
        except Exception as e:
            raise SourceLoadError(e)

        # store result
        self.loaded = dict([(k, traceback_wrapper(v)) for k, v in locals()["main"]().items()])

    def get(self, name=None):
        # no given name
        if name is None:
            if len(self.loaded) == 0:
                raise SourceVarDoesNotExistError("No variable was found in loaded source.")
            if len(self.loaded) > 1:
                raise MultipleSourceVarReturnedError(
                    "More than one variable was found, must provide a name to indicate which one to retrieve: %s"
                    % self.loaded.keys())
            return list(self.loaded.values())[0]

        # name is given
        if name not in self.loaded:
            raise SourceVarDoesNotExistError(
                "No variable named '%s' was found in loaded source. Available variables: %s"
                % (name, self.loaded.keys()))
        return self.loaded[name]
