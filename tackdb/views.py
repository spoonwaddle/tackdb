from collections import defaultdict


class RootViewException(Exception):
 
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


class DataView(object):

    """

    A DataView is a recursive key-value store which encapsulates data
    operations within transactions.

    Each DataView object has...
        1) an optional `parent` DataView, whose data can be read and commited to
        2) a local `scope` to stage data operations before committing to parent
        3) an internal cache to count distinct values

    A DataView without a parent set is considered to be the "root" DataView.
    A root node acts as the base case in recursively resolving key lookups and
    commiting data operations.

    """
    
    def __init__(self, parent=None, scope=None):
        self.parent = parent
        self.scope = scope or {}
        self.value_count_diff = defaultdict(int)

    @classmethod
    def wrap(cls, parent):
        return cls(parent=parent)

    @property
    def is_root(self):
        return self.parent is None
    
    def update_key(self, key, value):
        if value == None:
            self.delete_key(key)
        else:
            self.set_key(key, value)

    def update(self, updates):
        for k,v in updates.items():
            self.update_key(k, v)

    def set_key(self, key, value):
        try:
            old = self.GET(key)
            self.value_count_diff[old] -= 1
        except KeyError:
            pass
        finally:
            self.scope[key] = value
            self.value_count_diff[value] += 1

    def delete_key(self, key):
        try:
            value = self.GET(key)
            self.value_count_diff[value] -= 1
            if self.is_root:
                del self.scope[key]
                if self.value_count_diff[value] == 0:
                    del self.value_count_diff[value]
            else:
                self.scope[key] = None

        except KeyError:
            pass
    
    def merge_commit(self, child_scope):
        self.update(child_scope)
        if self.is_root:
            return self
        else:
            return self.parent.merge_commit(self.scope)
    
    def SET(self, key, value):
        self.set_key(key, value)

    def GET(self, key):
        if key in self.scope:
            if self.scope[key] is not None:
                return self.scope[key]
            else:
                raise KeyError("Key not found: {}".format(key))
        elif not self.is_root:
            return self.parent.GET(key)
        else:
            raise KeyError("Key not found: {}".format(key))

    def UNSET(self, key):
        self.delete_key(key)

    def BEGIN(self):
        return DataView.wrap(self)

    def ROLLBACK(self):
        if self.is_root:
            raise RootViewException("Cannot ROLLBACK root data view.")
        else:
            return self.parent

    def COMMIT(self):
        if self.is_root:
            raise RootViewException("Cannot COMMIT root data view.")
        else:
            return self.parent.merge_commit(self.scope)
    
    def NUMEQUALTO(self, value):
        own_diff = self.value_count_diff[value]
        if self.is_root:
            return own_diff
        else:
            return self.parent.NUMEQUALTO(value) + own_diff
