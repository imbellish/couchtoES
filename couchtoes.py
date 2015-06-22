import requests
import json
import logging

logging.basicConfig(filename="couchtoes.log", level=logging.DEBUG)


class CouchDB(object):

    @classmethod
    def connect(self, url="http://localhost:5984/", auth=None):
        if auth == None:
            return Connection(url=url)
        else:
            return Connection(url=url, auth=auth)


class Connection(object):

    def __init__(self, auth=None, url=None):
        self.auth = auth
        self.url = url
        if auth == None:
            self.status = requests.get(self.url)
        else:
            self.status = requests.get(self.url, auth=self.auth)
        #return self.status

    def isconnected(self):
        try:
            connection = self.status.status_code == 200
            return connection
        except:
            return False

    def close(self):
        self.status.close()
        del self.status

    def cursor(self):
        return Cursor(self)

class Cursor(object):

    def __init__(self, connection):
        self.connection = connection

    def __call__(self, view="_all_docs", method=None, params=None, dump=False):

        # for a straight cursor(view="myView", dump=True)
        if method == None and params == None and dump == True:

            if self.connection.auth:
                self.items = requests.get(self.connection.url+view, auth=self.connection.auth).json()
                self._items = self.items.__iter__()
            else:
                self.items = requests.get(self.connection.url+view).json()
        # TODO: incomplete logic
        elif params:
            self.items = requests.get(self.connection.url+view, auth=self.connection.auth, data=params).json()
            self._items = self.items.__iter__()

    def fetchone(self):
        return next(self._items)

    def fetchall(self):
        blob = []
        for doc in self._items:
            blob.append(doc)
        return blob



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