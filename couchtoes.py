import requests

import logging

logging.basicConfig(filename="couchtoes.log", level=logging.DEBUG)


class CouchDB(object):

    @classmethod
    def connect(self, url="http://localhost:5984/", auth=("admin", "admin"), ):
        return Connection(url=url, auth=auth)


class Connection(object):

    def __init__(self, auth=None, url=None):
        self.auth = auth
        self.url = url
        self.status = requests.get(self.url, auth=self.auth)

    def isconnected(self):
        try:
            connection = self.status.status_code == 200
            return connection
        except:
            return False

    def close(self):
        self.status.close()
        del self.status

    def cusor(self):
        return Cursor(self)

class Cursor(object):

    def __init__(self, connection, db):
        self.connection = connection

    def __call__(self, view="_all_docs", method='GET', params=None):
        if method == 'GET' and params == None:
            pass





class Error(Exception):
    pass

class Warning(Exception):
    pass

class InterfaceError(Error):
    pass

class DatabaseError(Error):
    pass

class InternalError(DatabaseError):
    pass

class OperationalError(DatabaseError):
    pass

class ProgrammingError(DatabaseError):
    pass

class IntegrityError(DatabaseError):
    pass

class DataError(DatabaseError):
    pass

class NotSupportedError(DatabaseError):
    pass