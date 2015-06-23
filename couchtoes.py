import requests
import json
import logging

logging.basicConfig(filename="couchtoes.log", level=logging.DEBUG)


class CouchDB(object):

    @classmethod
    def connect(self, **kwargs):
        return Connection(**kwargs)


class Connection(object):

    def __init__(self, auth=None, url=None, headers=None, params=None):
        self.auth = auth
        self.url = url
        self.headers = headers
        if auth == None:
            self.status = requests.get(self.url, headers=headers, params=params)
        else:
            self.status = requests.get(self.url, headers=headers, params=params, auth=self.auth)
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
        # keep it simple; start with a dump all from all docs
        if dump == True:
            self.items = requests.get(self.connection.url+"/"+view, headers=self.connection.headers).json()
            self._items = self.items['rows'].__iter__()
        elif params:
            self.items = requests.get(self.connection.url+"/"+view, headers=self.connection.headers, params=params).json()
            self._items = self.items["rows"].__iter__()

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