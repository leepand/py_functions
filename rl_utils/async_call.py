import requests
import queue
import threading

from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Mapping,
    NewType,
    Optional,
    Sequence,
    Set,
    TextIO,
    Tuple,
    Type,
    Union,
)


def async_call(target: Callable, timeout: Optional[int] = None) -> Callable:
    """Accepts a method and optional timeout.
    Returns a new method that will call the original with any args, waiting for upto timeout seconds.
    This new method blocks on the original and returns the result or None
    if timeout was reached, along with the thread.
    You can check thread.is_alive() to determine if a timeout was reached.
    If an exception is thrown in the thread, we reraise it.
    """
    q: "queue.Queue" = queue.Queue()

    def wrapped_target(q: "queue.Queue", *args: Any, **kwargs: Any) -> Any:
        try:
            q.put(target(*args, **kwargs))
        except Exception as e:
            q.put(e)

    def wrapper(
        *args: Any, **kwargs: Any
    ) -> Union[Tuple[Exception, "threading.Thread"], Tuple[None, "threading.Thread"]]:
        thread = threading.Thread(
            target=wrapped_target, args=(q,) + args, kwargs=kwargs
        )
        thread.daemon = True
        thread.start()
        try:
            result = q.get(True, timeout)
            if isinstance(result, Exception):
                raise result.with_traceback(sys.exc_info()[2])
            return result, thread
        except queue.Empty:
            return None, thread

    return wrapper


async_requests_get = async_call(requests.get, timeout=5)

pypi_url = "https://github.com/Chanzhaoyu/chatgpt-web/blob/main/src/components/business/Chat/layout/Layout.vue"
data, thread = async_requests_get(pypi_url, timeout=3)


def test(x):
    return x


d = async_call(test, timeout=5)
d("dsdf")
