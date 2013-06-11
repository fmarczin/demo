import py
import logging
from sqlalchemy import (
    create_engine, MetaData, Table, Column, String, select)


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='debug.log')


class FileDB(object):

    """FileDB object"""
    def __init__(self, dbpath=None):
        super(FileDB, self).__init__()
        if dbpath is None:
            dbpath = py.path.local.mkdtemp().join('users.db')
        self.dbpath = py.path.local(dbpath)
        self.usersfile = self.dbpath.join('users')
        self.usersfile.ensure(file=True)
        self.load()

    def load(self):
        self.users = dict(
            l.split(':') for l in self.usersfile.read().split('\n') if ':' in l)

    def save(self):
        self.usersfile.remove()
        self.usersfile.write('\n'.join(
            key + ':' + val for key, val in self.users.iteritems()))

    def __getitem__(self, userid):
        return self.users[userid]

    def __setitem__(self, userid, name):
        self.users[userid] = name
        self.save()

    def __delitem__(self, userid):
        del self.users[userid]
        self.save()

    def __contains__(self, userid):
        return userid in self.users


class SQLiteDB(object):

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
        self.engine = create_engine(dburl)
        self.meta = MetaData()
        self.users = Table(
            'users', self.meta,
            Column('id', String, primary_key=True),
            Column('name', String))
        self.meta.create_all(self.engine)
        self.conn = self.engine.connect()

    def __getitem__(self, userid):
        sel = select([self.users.c.name]).where(self.users.c.id == userid)
        res = self.conn.execute(sel).fetchone()
        return res[0]

    def __setitem__(self, userid, name):
        self.conn.execute(
            self.users.insert()
                .values(id=userid, name=name))

    def __delitem__(self, userid):
        self.conn.execute(self.users.delete().where(self.users.c.id == userid))

    def __contains__(self, userid):
        res = self.conn.execute(select([self.users.c.id]).where(
            self.users.c.id == userid)).fetchone()
        return (res is not None and res[0] is not None)
