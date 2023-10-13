import importlib
import types


class LazyLoader(types.ModuleType):
    def __init__(self, module_name="os", submod_name=None):
        self._module_name = "{}{}".format(
            module_name, submod_name and ".{}".format(submod_name) or ""
        )
        self._mod = None
        super(LazyLoader, self).__init__(self._module_name)

    def _load(self):
        if self._mod is None:
            self._mod = importlib.import_module(self._module_name)
        return self._mod

    def __getattr__(self, attrb):
        return getattr(self._load(), attrb)

    def __dir__(self):
        return dir(self._load())


_os = LazyLoader("os")
_os.listdir("./")
