import pytest
import filedb


@pytest.fixture(params=['FileDB', 'SQLiteDB'])
def dbclass(request):
    return getattr(filedb, request.param)


def test_init(dbclass, tmpdir):
    assert dbclass() is not None
    assert dbclass(tmpdir) is not None


@pytest.fixture()
def cleandb(dbclass, tmpdir):
    db = dbclass(tmpdir)
    return db


@pytest.fixture
def userdb(cleandb):
    users = {
        'user1': 'User 1',
        'user2': 'User 2',
        'user3': 'User 3'
    }
    for userid, name in users.iteritems():
        cleandb[userid] = name
    return cleandb


def test_add(cleandb):
    cleandb['user1'] = 'User 1'
    cleandb['user2'] = 'User 2'
    assert ('user1' in cleandb) and ('user2' in cleandb)


def test_find(userdb):
    assert 'user1' in userdb
    assert 'user2' in userdb
    assert not 'dummy' in userdb


def test_get(userdb):
    assert userdb['user1'] is not None


def test_remove(userdb):
    assert 'user1' in userdb
    del userdb['user1']
    assert not 'user1' in userdb
