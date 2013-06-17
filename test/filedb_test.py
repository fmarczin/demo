import pytest
import filedb


@pytest.fixture(params=['FileDB', 'SQLiteDB'])
def dbclass(request):
    return getattr(filedb, request.param)


def test_init(dbclass, tmpdir, monkeypatch):
    monkeypatch.chdir(tmpdir)
    assert dbclass() is not None
    assert dbclass(tmpdir) is not None


@pytest.fixture()
def cleandb(dbclass, tmpdir):
    db = dbclass(tmpdir)
    return db


@pytest.fixture
def userdb(cleandb):
    demousers = {
        'user1': 'User 1',
        'user2': 'User 2',
        'user3': 'User 3'
    }
    for userid, name in demousers.iteritems():
        cleandb[userid] = name
    return cleandb


def test_set(cleandb):
    cleandb['user1'] = 'User 1'
    cleandb['user2'] = 'User 2'


def test_contains(cleandb):
    cleandb['user1'] = 'User 1'
    cleandb['user2'] = 'User 2'
    assert 'user1' in cleandb
    assert 'user2' in cleandb
    assert not 'dummy' in cleandb


def test_retrieve(cleandb):
    cleandb['user1'] = 'User 1'
    cleandb['user2'] = 'User 2'
    assert cleandb['user1'] == 'User 1'
    assert cleandb['user2'] == 'User 2'


def test_remove(userdb):
    assert 'user1' in userdb
    del userdb['user1']
    assert not 'user1' in userdb


def test_persist(dbclass, tmpdir):
    db1 = dbclass(tmpdir)
    db1['user1'] = 'User 1'
    db1['user2'] = 'User 2'
    del db1
    db2 = dbclass(tmpdir)
    assert db2['user1'] == 'User 1'
    assert db2['user2'] == 'User 2'
