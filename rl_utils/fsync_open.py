import contextlib
import pathlib
import os

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


@contextlib.contextmanager
def fsync_open(
    path: Union[pathlib.Path, str], mode: str = "w", encoding: Optional[str] = None
) -> Generator[IO[Any], None, None]:
    """
    Opens a path for I/O, guaranteeing that the file is flushed and
    fsynced when the file's context expires.
    """
    with open(path, mode, encoding=encoding) as f:
        yield f

        f.flush()
        os.fsync(f.fileno())


with fsync_open("fsync_open.txt", "w") as file:
    file.write("data")
