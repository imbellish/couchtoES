import requests
import json
import logging
import configparser

logging.basicConfig(filename="couchtoes.log", level=logging.DEBUG)

# TODO: set config files
"""
config = configparser.ConfigParser()
URL = config.get("db", "base_url")
"""
class CouchDB(object):
    """
    Example usage as per PEP 0249 https://www.python.org/dev/peps/pep-0249/

    from couchtoes import CouchDB
    db = CouchDB.connect(url="localhost:5984/db", headers={"User-Agent":"admin:admin"})
    cursor = db.cursor()
    cursor(view="_all_docs", params={"limit":1}
    row = cursor.fetchone()

    """

    @classmethod
    def connect(self, **kwargs):
        return Connection(**kwargs)


class Connection(object):

    def __init__(self, auth=None, url=None, headers=None, params=None):
        self.auth = auth
        self.url = url
        self.headers = headers
        if auth is None:
            self.status = requests.get(
                self.url,
                headers=headers,
                params=params)
        else:
            self.status = requests.get(
                self.url,
                headers=headers,
                params=params,
                auth=self.auth)
        # return self.status

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
        self.current_view = None
        logging.debug("Creating cursor")

    def __call__(self, view=None, method=None, params=None, dump=False):

        # for a straight cursor(view="myView", dump=True)
        # keep it simple; start with a dump all from all docs
        #self.current_view = view
        if not view and not self.current_view:
            logging.debug("View not set. Going to default.")
            self.current_view = "pronot_spartan/_all_docs"
        elif not view:
            logging.debug("not setting a view. rely on default. ")
            pass
        else:
            # only reassigns self.view when passed
            logging.debug("Setting called view to default view.")
            self.current_view = view

        if dump == True:
            self.items = requests.get(
                self.connection.url +
                "/" +
                self.current_view,
                headers=self.connection.headers,
                params=params).json()
            self._items = self.items['rows'].__iter__()
        # basic parameters on views
        elif params:
            self.items = requests.get(
                self.connection.url +
                "/" +
                self.current_view,
                headers=self.connection.headers,
                params=params).json()
            self._items = self.items["rows"].__iter__()
        elif method:
            raise NotImplementedError("cursor is restricted to GET's")

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

if __name__ == "__main__":

    from pprint import pprint

    class memo:
        pass

    # default config
    db = CouchDB.connect(
        url="http://localhost:5984",
        headers={
            "User-Agent": "admin:admin"})

    cursor = db.cursor()
    default_view = "pronot_spartan/_all_docs"
    options = [
        "(s) search",
        "(d) dump",
        "(q) quit"
    ]
    fmt = "Select an option: {0}, {1}, {2}".format(*options)
    while True:
        print(fmt)
        user = input("\n")
        if user == "q":
            break
        elif user == "s":
            while True:
                search_options = [
                    "(cursor parameters) execute",
                    "(q) quit"
                ]
                search_option = input("{0}, {1} : ".format(*search_options))
                if search_option == "q":
                    break
                else:
                    try:
                        exec('cursor(' + search_option + ')')
                    except Error as e:
                        print(e.__name__ + "occured")
                    pprint(cursor.fetchall())
        elif user == "d":
            to_file = input("Name of the dump file: ")
            params = {'include_docs': True}
            cursor(view=default_view, dump=True, params=params)
            f = open(to_file, 'w')
            f.write(str(cursor.items))
            f.close()
            print("dump completed. see " + to_file)
