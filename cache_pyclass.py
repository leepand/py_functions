#https://github.com/ottogroup/palladium/blob/f02d8e28889383ae5842225725e301c9182461bf/palladium/util.py
try:
    from collections import UserDict
except:
    from UserDict import UserDict
from datetime import datetime
class ProcessStore(UserDict,object):
    def __init__(self, *args, **kwargs):
        self.mtime = {}
        super(ProcessStore, self).__init__(*args, **kwargs)

    def __setitem__(self, key, item):
        super(ProcessStore, self).__setitem__(key, item)
        self.mtime[key] = datetime.now()

    def __getitem__(self, key):
        return super(ProcessStore, self).__getitem__(key)

    def __delitem__(self, key):
        super(ProcessStore, self).__delitem__(key)
        del self.mtime[key]


process_store = ProcessStore(process_metadata={})
cache = process_store
class data(object):
    def __init__(self):
        print 'sd'
    def _find(self):
        return 5
x=data()
cache['self.key'] = x
cache
