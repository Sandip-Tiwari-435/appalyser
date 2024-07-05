from utils import hash_password
import sqlite3
import streamlit as st
import pymongo
from datetime import datetime

@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets['mongo']['url'])

client=init_connection()

def createSession(username,allowedRetries,summaryRetries):
    st.session_state['user_authenticated'] = True
    st.session_state['username'] = username
    st.session_state.summaryFree=int(summaryRetries)
    st.session_state.searchFree=int(allowedRetries)
    st.session_state.cookies["logged_in"]="true"
    st.session_state.cookies["username"]=username
    st.session_state.cookies["summaryFree"]=str(summaryRetries)
    st.session_state.cookies["searchFree"]=str(allowedRetries)

def create_user(username,password,email,paid=0):
    try:
        allowedRetries=1000 if paid==1 else 7
        summaryRetries=1000 if paid==1 else 7
        coll=client.user_database.users
        coll.insert_one({
            "username":username,
            "password":hash_password(password),
            "email":email,
            "allowedRetries":allowedRetries,
            "summaryRetries":summaryRetries,
            "created_at":datetime.now()
            })
        print(hash_password(password))
        st.success('User created. Signing in...')
        createSession(username,allowedRetries,summaryRetries)
    except Exception as e:
        print(f'the createUser exception was {e}')
        return False
    return True

def authenticate_user(username,password):
    try:
        coll=client.user_database.users
        result = coll.find_one({'username':username})
        print(result['password'])
        print(hash_password(password))
        if len(list(result))!=0 and result['password'] == hash_password(password):
            createSession(username,result['allowedRetries'],result['summaryRetries'])
            return True
    except Exception as e:
        print(f'the authenticate exception is {e}')
    return False

def update_user(username):
    try:
        coll=client.user_database.users
        filter={'username':username}
        updated_field={'$set':{
            'allowedRetries':st.session_state.searchFree,
            'summaryRetries':st.session_state.summaryFree,
            }}
        coll.update_one(filter,updated_field)
    except Exception as e:
        print(f'the updateuser exception is {e}')
        return False
    return True 

def check_duplicate(username):
    try:
        coll=client.user_database.users
        filter={'username':username}
        results=coll.find(filter)
        if len(list(results)):
            return True
    except Exception as e:
        print(f'the checkDup exception is {e}')
    return False

def get_comments(offset=0,limit=10):
    try:
        coll=client.user_database.comments
        results=coll.find().sort('created_at',-1).limit(limit).skip(offset)
        finalResult=[]
        for result in results:
            finalResult.append([result['username'],result['created_at'],result['comment']])
        return finalResult
    except Exception as e:
        print(f'the getComm exception is {e}')
    return []

def add_comment(username,comment):
    try:
        coll=client.user_database.comments
        coll.insert_one({
            'username':username,
            'comment':comment,
            'created_at':datetime.now()
            })
    except Exception as e:
        print(f'the addComment exception is {e}')
        return False
    return True
