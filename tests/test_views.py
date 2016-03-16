import pytest
from tackdb.views import DataView

def test_root():
    a = DataView()
    b = a.BEGIN()
    assert a.is_root and not b.is_root


def test_update():
    a = DataView()
    a.SET('burger', 'cheese')
    a.SET('fries', 'chili cheese')
    updates = {'shake': 'chocolate', 'burger': None, 'fries': 'plain'}
    
    a.update(updates)
    
    assert a.GET('shake') == 'chocolate'
    assert a.GET('fries') == 'plain'
    with pytest.raises(KeyError):
        a.GET('burger')
    assert a.NUMEQUALTO('cheese') == 0
    assert a.NUMEQUALTO('chilli cheese') == 0

def test_set_new_key_root():
    a = DataView()
    a.SET('oh', 'hello')
    assert a.GET('oh') == 'hello'
    assert a.NUMEQUALTO('hello') == 1


def test_replace_key_root():
    a = DataView()
    a.SET('oh', 'hello')
    a.SET('oh', 'well')
    assert a.GET('oh') == 'well'
    assert a.NUMEQUALTO('well') == 1
    assert a.NUMEQUALTO('hello') == 0


def test_unset():
    a = DataView()
    a.SET('good', 'bye')
    a.UNSET('good')
    with pytest.raises(KeyError):
        a.GET('good')
    assert a.NUMEQUALTO('good') == 0


"""
transactiony fun begins here
"""

def test_begin():
    a = DataView()
    assert a.BEGIN().parent is a


def test_rollback():
    a = DataView()
    a.SET('porous', 'true')
    a.SET('pants_shape', 'square')
    a = a.BEGIN()
    a.SET('pants_shape', 'round')
    a = a.ROLLBACK()
    assert a.GET('pants_shape') == 'square'
    assert a.GET('porous') == 'true'


def test_commit():
    a = DataView()
    a.SET('porous', 'true')
    a.SET('pants_shape', 'square')
    a = a.BEGIN()
    a.SET('pants_shape', 'round')
    a = a.COMMIT()
    assert a.GET('pants_shape') == 'round'
    assert a.GET('porous') == 'true'


def test_downstream_get():
    parent = DataView()
    parent.SET('last', 'simpson')
    parent.SET('first', 'abe')
    child = parent.BEGIN()
    child.SET('first', 'homer')
    assert child.GET('first') == 'homer'
    assert parent.GET('first') == 'abe'
    assert child.GET('last') == 'simpson'
    assert child.NUMEQUALTO('abe') == 0
    assert child.NUMEQUALTO('homer') == 1
