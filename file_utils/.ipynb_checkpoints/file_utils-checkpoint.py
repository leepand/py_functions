import os
import errno

ENCODING = "utf-8"


def is_directory(name):
    return os.path.isdir(name)


def is_file(name):
    return os.path.isfile(name)

def exists(name):
    return os.path.exists(name)

def list_all(root, filter_func=lambda x: True, full_path=False):
    """
    List all entities directly under 'dir_name' that satisfy 'filter_func'
    :param root: Name of directory to start search
    :param filter_func: function or lambda that takes path
    :param full_path: If True will return results as full path including `root`
    :return: list of all files or directories that satisfy the criteria.
    """
    if not is_directory(root):
        raise Exception("Invalid parent directory '%s'" % root)
    matches = [x for x in os.listdir(root) if filter_func(os.path.join(root, x))]
    return [os.path.join(root, m) for m in matches] if full_path else matches
def list_subdirs(dir_name, full_path=False):
    """
    Equivalent to UNIX command:
      ``find $dir_name -depth 1 -type d``
    :param dir_name: Name of directory to start search
    :param full_path: If True will return results as full path including `root`
    :return: list of all directories directly under 'dir_name'
    """
    return list_all(dir_name, os.path.isdir, full_path)


def list_files(dir_name, full_path=False):
    """
    Equivalent to UNIX command:
      ``find $dir_name -depth 1 -type f``
    :param dir_name: Name of directory to start search
    :param full_path: If True will return results as full path including `root`
    :return: list of all files directly under 'dir_name'
    """
    return list_all(dir_name, os.path.isfile, full_path)


def find(root, name, full_path=False):
    """
    Search for a file in a root directory. Equivalent to:
      ``find $root -name "$name" -depth 1``
    :param root: Name of root directory for find
    :param name: Name of file or directory to find directly under root directory
    :param full_path: If True will return results as full path including `root`
    :return: list of matching files or directories
    """
    path_name = os.path.join(root, name)
    return list_all(root, lambda x: x == path_name, full_path)

def mkdir(root, name=None):
    """
    Make directory with name "root/name", or just "root" if name is None.
    :param root: Name of parent directory
    :param name: Optional name of leaf directory
    :return: Path to created directory
    """
    target = os.path.join(root, name) if name is not None else root
    try:
        os.makedirs(target)
    except OSError as e:
        if e.errno != errno.EEXIST or not os.path.isdir(target):
            raise e
    return target

mkdir("tmp","aah2")
is_directory("tmp/aah2")
exists("tmp/aah2")
list_all("tmp",full_path=True)
find("tmp","aah",full_path=True)
