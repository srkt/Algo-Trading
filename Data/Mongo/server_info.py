from Data.Mongo.database import MongoServer

database_name = 'equitydb'

server = MongoServer()
server.set_database_name(database_name)
