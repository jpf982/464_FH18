#for testing of pymongo code
import pymongo
from pymongo import MongoClient

#Provide the mongoDB ATLAS url to connect pythong to mongodb using pymongo
CONNECTION_STRING = "mongodb+srv://jFoster:464FH18@464fh18.wbhrb.mongodb.net/464FH18?retryWrites=true&w=majority"
#create a connection to the cluster using MongoCleint 
cluster = MongoClient(CONNECTION_STRING)
#access database in cluster
db = cluster["DataBase1"]
#access collection in database 
collection = db["test"]

#How to add data to the collection:
#created documents should always include: {"_id": Unqiue#,...} to ensure a random ObjectID is not generated instead
#post = {"_id": 0, "name":"Jim", "age":22}
#insert one document to the accessed collection
#collection.insert_one(post)
#delete one document from the accessed collection
#collection.delete_one(post)

#Multiple documents can be added at the same time:
#doc1 = {"_id": 1, "name":"Charles", "age": 24}
#doc2 = {"_id": 2, "name":"Patrick", "age": 58}
#insert multiple documents to the accessed collection
#collection.insert_many([doc1, doc2])
#delete multiple documents from the accessed collection
#collection.delete_many([post, doc1, doc2])
