import streamlit as st
from utils import select_role
import configparser
from genAi import model,consumerContext,developerContext
from role import Role
from auth import get_comments
from streamlit_cookies_manager import EncryptedCookieManager
import requests
# import os

def main():
    st.set_page_config(page_title="Appalyser", page_icon="📱")
    config=configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    # tokens
    try:
        if 'cookies' not in st.session_state:
            tookies=EncryptedCookieManager(
                    prefix="my_app_",
                    password="92ee0278-28f0-4bfd-b23c-76f707b4c347",
                )
            if not tookies.ready():
                st.stop()
            st.session_state.cookies=tookies

        if "DEVELOPER_ROLE" not in st.session_state:
            st.session_state.DEVELOPER_ROLE = Role(name="Developer", permissions=["analyze", "debug"], usage="Provide technical suggestions", context=developerContext, chatplaceholder='How to fix network issues in my app', chat = model.start_chat(history=developerContext), home=["the competition of your next app", "Discuss what can be improved in an app and how. The path to success of your next app!"])
        if "CONSUMER_ROLE" not in st.session_state:
            st.session_state.CONSUMER_ROLE = Role(name="Consumer", permissions=["use", "feedback"], usage="Provide practical usage suggestions", context=consumerContext, chatplaceholder='How to save battery while using Spotify', chat = model.start_chat(history=consumerContext), home=["your favourite apps","Discuss on how to solve your issue with an app quickly and with ease. Be as detailed as possible"]) 
        if 'responselength' not in st.session_state:
            st.session_state.responselength=200
        if 'sumbit' not in st.session_state:
            st.session_state.submit=False
        if 'review' not in st.session_state:
            st.session_state.review={}
        if 'summaries' not in st.session_state:
            st.session_state.summaries={
                    "Developer":{},
                    "Consumer":{}
                    }
        if 'summaryFree' not in st.session_state:
            st.session_state.summaryFree=int(st.session_state.cookies["summaryFree"]) if 'summaryFree' in st.session_state.cookies else int(config['Playground']['free_summary_usage'])
        if 'searchFree' not in st.session_state:
            st.session_state.searchFree=int(st.session_state.cookies["searchFree"]) if 'searchFree' in st.session_state.cookies else int(config['Playground']['free_search_usage'])
        if 'user_authenticated' not in st.session_state:
            st.session_state['user_authenticated'] = False
        # if 'ip' not in st.session_state:
        #     try:
        #         st.session_state['ip']=requests.get('https://api64.ipify.org?format=json').json()['ip']
        #     except Exception as e:
        #         os.write(1,f"Error in session states {e}")
        #     os.write(1,f"The ip of this user: {st.session_state['ip']}")
        if 'username' not in st.session_state:
            st.session_state['username'] = 'Anon'
        if 'new_username' not in st.session_state:
            st.session_state['new_username']='poki'
        if 'new_password' not in st.session_state:
            st.session_state['new_password']='poki'
        if 'new_email' not in st.session_state:
            st.session_state['new_email']=''
        if 'current_page' not in st.session_state:
            st.session_state['current_page']='Home'
        if 'csv' not in st.session_state:
            st.session_state.csv=False
        if 'spreadsheet_id' not in st.session_state:
            st.session_state.spreadsheet_id=''
        if 'offset' not in st.session_state:
            st.session_state.offset = 0
        if 'page_config' in st.session_state:
            st.session_state['page_config']=True
        if 'comments' not in st.session_state:
            st.session_state.comments = get_comments(st.session_state.offset, 10)
        if 'usingAppStoreScraper' not in st.session_state:
            st.session_state.usingAppStoreScraper=True
        if 'myDict' not in st.session_state:
            st.session_state.myDict=[]
        if "messages" not in st.session_state:
            st.session_state.messages = {
                "Developer":[
                    {
                        "role":"assistant",
                        "content":"Ask me Anything like how to fix a bug in an app"
                    }
                ],
                "Consumer":[
                    {
                        "role":"assistant",
                        "content":"Ask me Anything like why is battery draining while using Spotify app"
                    }
                ]
            }

    except Exception as e:
        print("Error occured while initialising the application {}",e)
    finally:
        select_role()
        if 'logged_in' in st.session_state.cookies and st.session_state.cookies['logged_in']:
            st.session_state.user_authenticated = True
            st.session_state.cookies['summaryFree']=str(st.session_state.summaryFree)
            st.session_state.cookies['searchFree']=str(st.session_state.searchFree)
            st.session_state.username = st.session_state.cookies["username"]
        else:
            st.session_state.user_authenticated = False
            st.session_state.cookies['summaryFree']=str(st.session_state.summaryFree)
            st.session_state.cookies['searchFree']=str(st.session_state.searchFree)
        st.session_state.cookies.save()
