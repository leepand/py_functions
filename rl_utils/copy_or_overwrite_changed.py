import platform
import shutil
import os
import stat
from typing import BinaryIO, Union
from mlopskit.pastry.utils import mkdir_exists_ok

StrPath = Union[str, "os.PathLike[str]"]

WRITE_PERMISSIONS = stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH | stat.S_IWRITE


def copy_or_overwrite_changed(source_path: StrPath, target_path: StrPath) -> StrPath:
    """Copy source_path to target_path, unless it already exists with the same mtime.
    We liberally add write permissions to deal with the case of multiple users needing
    to share the same cache or run directory.
    Args:
        source_path: The path to the file to copy.
        target_path: The path to copy the file to.
    Returns:
        The path to the copied file (which may be different from target_path).
    """
    return_type = type(target_path)

    if platform.system() == "Windows":
        head, tail = os.path.splitdrive(str(target_path))
        if ":" in tail:
            logger.warning("Replacing ':' in %s with '-'", tail)
            target_path = os.path.join(head, tail.replace(":", "-"))

    need_copy = (
        not os.path.isfile(target_path)
        or os.stat(source_path).st_mtime != os.stat(target_path).st_mtime
    )

    permissions_plus_write = os.stat(source_path).st_mode | WRITE_PERMISSIONS
    if need_copy:
        mkdir_exists_ok(os.path.dirname(target_path))
        try:
            # Use copy2 to preserve file metadata (including modified time).
            shutil.copy2(source_path, target_path)
        except PermissionError:
            # If the file is read-only try to make it writable.
            try:
                os.chmod(target_path, permissions_plus_write)
                shutil.copy2(source_path, target_path)
            except PermissionError as e:
                raise PermissionError("Unable to overwrite '{target_path!s}'") from e
        # Prevent future permissions issues by universal write permissions now.
        os.chmod(target_path, permissions_plus_write)

    return return_type(target_path)  # type: ignore  # 'os.PathLike' is abstract.

copy_or_overwrite_changed("fsync_open.txt","./fsync_open2.txt")

