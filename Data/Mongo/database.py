import pymongo
import pandas as pd

server = '172.23.6.124:27017/'


class MongoServer():

    def __init__(self, server_prefix='mongodb://', host_name='localhost', port=27017):

        self.server_prefix = server_prefix
        self.host_name = host_name
        self.port = port

        self.server_name = self.server_prefix + self.host_name + ':' + str(self.port)

    def set_database_name(self, name):
        if not name:
            raise Exception('Invalid database name')

        self.databasename = name

    def _getclient(self):
        client = pymongo.MongoClient(self.server_name)
        return client

    def get_database(self, database_name=None):

        if not database_name:
            raise Exception('Database name not set');

        client = self._getclient()

        db_list = client.list_database_names()

        if database_name in db_list:
            print('Connecting to database ' + database_name)
        else:
            print(database_name + 'not existing')

        if not database_name:
            return client[self.databasename]
        else:
            return client[database_name]

    def get_collection(self,
                       collection_name,
                       database_name=None):

        if not database_name:
            if not self.databasename:
                raise Exception('Please provide database name or set database name on server instance')
            else:
                database_name = self.databasename

        database = self.get_database(database_name)
        return database[collection_name]

    def get_dataframe_from_collection(self,
                                      collection_name,
                                      database_name=None,
                                      query={},
                                      projection={"_id": 0}):

        if not collection_name:
            raise Exception('invalid collection name')

        if not isinstance(query, dict):
            raise Exception('query should be of type dictionary')

        if not isinstance(projection, dict):
            raise Exception('projection should be of type dictionary')

        collection = self.get_collection(collection_name, database_name)
        data = collection.find(query, projection)
        df = pd.DataFrame(list(data))
        return df
