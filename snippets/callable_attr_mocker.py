"""
opysnippets/callable_attr_mocker:1.0.0
"""
import logging

logger = logging.getLogger(__name__)


class CallableAttrMocker:
    """
    will return a function accepting all attrs and kwargs, having no effect when called
    """
    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, item):
        def fct(*args, **kwargs):
            logger.info(
                "CallableAttrMocker function called." '%s',
                extra=dict(
                    item=item,
                    args=str(args),
                    kwargs=str(kwargs)
                )
            )
        return fct
