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
        cleandb.user_add(userid, name)
    return cleandb


def test_add(cleandb):
    cleandb.user_add('user1', 'User 1')
    cleandb.user_add('user2', 'User 2')
    assert cleandb.user_exists('user1') and cleandb.user_exists('user2')


def test_find(userdb):
    assert userdb.user_exists('user1')
    assert userdb.user_exists('user2')
    assert not userdb.user_exists('dummy')


def test_get(userdb):
    assert userdb.user_get('user1') is not None


def test_remove(userdb):
    assert userdb.user_exists('user1')
    userdb.user_del('user1')
    assert not userdb.user_exists('user1')
