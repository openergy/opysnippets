"""
opysnippets/ologging:1.0.0

Openergy's logging library.
Logging should be done using python's logging library, like below:

logger = logging.get_logger(__name__)
logger.warning(<message>, extra=<properties>)

where <message> is a generic log message (it should not contain any variable)
and <properties> is a dictionnary containing user-defined information useful for debugging (as an example:
{'client_ip': '10.0.0.1', 'user_id': 12345, analysis_id: 21323123})

Properties must be str, int or float.
For message, 1st sentence is lowercase. If no other sentence, no point. Else put a point and use uppercase for beginning
of other sentences.

Handlers using the TextFormatter class as a formatter will get the properties at the end of the logging message.

The AzureLoggingHandler is used to have logs sent to azure application insights.
"""
import logging
import textwrap

RESERVED_ATTRS = (
    "args", "asctime", "created", "exc_info", "exc_text", "filename", "funcName", "levelname", "levelno", "lineno",
    "module", "msecs", "message", "msg", "name", "pathname", "process", "processName", "relativeCreated", "stack_info",
    "thread", "threadName"
)


class TextFormatter(logging.Formatter):
    def format(self, record):
        """Formats a log record and serializes to json"""
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        # add the extra fields
        if s[-1:] != "\n":
            s = s + "\n"
        s = s + textwrap.indent(
            '\n'.join([f'{key} : {record.__dict__[key]}' for key in record.__dict__ if key not in RESERVED_ATTRS]),
            '  |'
        )
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != "\n":
                s = s + "\n"
            s = s + self.formatStack(record.stack_info)
        return s
