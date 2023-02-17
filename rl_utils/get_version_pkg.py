import pkg_resources
def get_version(module_name):
    ''' Check if the python environment has installed the module or package.
        return the version of the module if the module is installed,
        return None otherwise.
    Args:
        module_name (str): module to be checked
    Returns:
        has_module: str (if the module is installed) or None
    '''
    assert isinstance(module_name, str), '"module_name" should be a string!'
    try:
        __import__(module_name)
    except ImportError:
        return None
    else:
        module_version = pkg_resources.get_distribution(module_name).version
        return module_version
get_version("numpy")
