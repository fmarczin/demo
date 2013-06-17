import py
import logging
from sqlalchemy import (
    create_engine, MetaData, Table, Column, String, select)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='debug.log')


class FileDB(dict):

    """FileDB object"""
    def __init__(self, *args, **kwargs, dbpath=None):
        if dbpath and (args or kwargs):

        super(FileDB, self).__init__()
        if dbpath is None:
            dbpath = py.path.local('.').join('users.db')
        self._dbpath = py.path.local(dbpath)
        self._usersfile = self._dbpath.join('users')
        self._usersfile.ensure(file=True)
        self._load()

    def _load(self):
        self._users = dict(
            l.split(':') for l in self._usersfile.read().split('\n') if ':' in l)

    def _save(self):
        self._usersfile.remove()
        self._usersfile.write('\n'.join(
            key + ':' + val for key, val in self._users.iteritems()))

    def __getitem__(self, userid):
        return self._users[userid]

    def __setitem__(self, userid, name):
        self._users[userid] = name
        self._save()

    def __delitem__(self, userid):
        del self._users[userid]
        self._save()

    def __contains__(self, userid):
        return userid in self._users


class SQLiteDB(dict):

    """SQLiteDB object"""
    def __init__(self, dbpath=None):
        super(SQLiteDB, self).__init__()

        self.dbpath = py.path.local(dbpath)
        if dbpath is None:
            self.userdbpath = ':memory:'
        else:
            self.userdbpath = self.dbpath.join('users.db')
        dburl = 'sqlite:///' + str(self.userdbpath)
        log.debug('dburl: ' + dburl)
        engine = create_engine(dburl)
        meta = MetaData()
        self._users = Table(
            'users', meta,
            Column('id', String, primary_key=True),
            Column('name', String))
        meta.create_all(engine)
        self._conn = engine.connect()

    def __getitem__(self, userid):
        sel = select([self._users.c.name]).where(self._users.c.id == userid)
        res = self._conn.execute(sel).fetchone()
        return res[0]

    def __setitem__(self, userid, name):
        self._conn.execute(
            self._users.insert()
                .values(id=userid, name=name))

    def __delitem__(self, userid):
        self._conn.execute(self._users.delete().where(self._users.c.id == userid))

    def __contains__(self, userid):
        res = self._conn.execute(select([self._users.c.id]).where(
            self._users.c.id == userid)).fetchone()
        return (res is not None and res[0] is not None)
