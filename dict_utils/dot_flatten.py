import importlib
from logging import getLogger

log = getLogger(__name__)


def dot_flatten(d):
    try:
        from flatten_dict import flatten

        d = flatten(d, reducer="dot", enumerate_types=(list,))
    except Exception:
        log.warning(
            "{} failed to be flattened. To install dependency, you can run: pip install flatten-dict>=0.3.0".format(
                d
            ),
            exc_info=True,
        )
    return d


dot_flatten({"x": {"y": 0}})
