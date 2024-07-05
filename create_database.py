from pymongo import MongoClient
from datetime import datetime
def setup_userdb():
    client=MongoClient(st.secrets['mongo']['url'])
    db=client['user_database']
    
    if 'users' not in db.list_collection_names():
        db.create_collection('users', validator={
                 '$jsonSchema': {
                     'bsonType': 'object',
                     'required': ['username', 'password', 'email'],
                     'properties': {
                         'username': {'bsonType': 'string'},
                         'password': {'bsonType': 'string'},
                         'email': {'bsonType': 'string'},
                         'searchRetries': {'bsonType': 'int'},
                         'summaryRetries': {'bsonType': 'int'},
                         'created_at':{'bsonType':'date'}
                     }
                 }
             })
        db['users'].create_index([('username',1)],unique=True)

def setup_commdb():
    client=MongoClient('mongodb+srv://sandipt335:4q0WU7BW9kW5uXkX@cluster0.mm9pw6p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0',server_api=ServerApi('1'))
    db = client['user_database']
    if 'comments' not in db.list_collection_names():
        db.create_collection('comments', validator={
            '$jsonSchema': {
                'bsonType': 'object',
                'required': ['username', 'comment'],
                'properties': {
                    'username': {'bsonType': 'string'},
                    'comment': {'bsonType': 'string'},
                    'created_at': {'bsonType': 'date'}
                }
            }
        })

