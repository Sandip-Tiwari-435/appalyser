import json
import requests
import re
import threading
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from app_store_scraper import AppStore
from gsheetUploader import gsheetUpload
import queue
import streamlit as st

def extractFromAppUrl(url):
    html_source=requests.get(url)
    soup = BeautifulSoup(html_source.text, 'html.parser')
    element = soup.find(class_='we-rating-count star-rating__count')
    text_content = element.get_text().split(' ')
    return (text_content[0],float(text_content[2])*100 if text_content[2][-1].isdigit() else str(float(text_content[2][:-1])*100)+text_content[2][-1])

def clean_string(input_string):
    cleaned_string = re.sub(r'[^\w\s]', '_', input_string)
    cleaned_string = re.sub(r'\s', '', cleaned_string)
    return cleaned_string

def csvGenerator(name,app_id,how_many):
    data = AppStore(country='us', app_name=name, app_id=app_id)
    data.review(how_many=how_many)
    print(f"The data is {data}")
    sorted_reviews = sorted(data.reviews, key=lambda x: int(x['rating']), reverse=False)

    limited_data = sorted_reviews[:how_many]
    data1 = pd.DataFrame(np.array(limited_data),columns=['review'])
    if data1.empty==False:
        data2 = data1.join(pd.DataFrame(data1.pop('review').tolist()))
        data2 = data2.sort_values('rating', ascending=True)
        Shopee = data2[['rating','userName','review','date']]
        return {"name":name,"df":Shopee}

def perform_upload(spreadsheet_id, myDict, j):
    try:
        gsheetUpload(spreadsheet_id, myDict, j)
        return True  
    except requests.HTTPError as e:
        return False

def retry_upload(spreadsheet_id, myDict, j, max_retries=3, retry_delay=15):
    retries = 0
    while retries < max_retries:
        if perform_upload(spreadsheet_id, myDict, j):
            return True  
        retries += 1
        time.sleep(retry_delay)  
    return False  


def gsheet_upload_worker(upload_queue):
    while True:
        try:
            spreadsheet_id, myDict, j = upload_queue.get()
            if myDict is None:
                break
            (a,b)=extractFromAppUrl(myDict["appUrl"])
            myDict["overallRating"]=a
            myDict["totalDownloads"]=str(b)+"+"
            gsheetUpload(spreadsheet_id,myDict,j)
            upload_queue.task_done()
        except requests.HTTPError as http_err:
            success = retry_upload(spreadsheet_id, myDict, j)
        except Exception as e:
            return

def gsheetCacher(countOfReviews,myDict,lino):
    index=0
    upload_queue = queue.Queue()
    upload_thread = threading.Thread(target=gsheet_upload_worker, args=(upload_queue,))
    upload_thread.start()
    try:
        for i in myDict:
            j=lino[index]
            upload_queue.put((st.session_state.spreadsheet_id,myDict[index],j))
            index+=1
    except Exception as e:
        print(f"ok exception {e}")
    upload_queue.put((None, None, None))
    return

def gsheetThreader(countOfReviews,myDict):
    index=0
    print("in gsheet")
    if len(st.session_state.spreadsheet_id)!=0:
        upload_queue = queue.Queue()
        upload_thread = threading.Thread(target=gsheet_upload_worker, args=(upload_queue,))
        upload_thread.start()
    for i in myDict:
        j = csvGenerator(i["name"],i["id"],countOfReviews)
        yield j
        if len(st.session_state.spreadsheet_id)!=0:
            upload_queue.put((st.session_state.spreadsheet_id,myDict[index],j))
        index+=1
    if len(st.session_state.spreadsheet_id)!=0:
        upload_queue.put((None, None, None))


def appStoreScraper(name,countOfReviews):
    st.session_state.usingAppStoreScraper=True
    print("here in appstore")
    try:
        html_source=requests.get(f"https://www.apple.com/in/search/{name}?src=serp")
    except:
        return
    pattern = re.compile(r'window\.pageLevelData\.searchResults\.searchData\s*=\s*({.*?});', re.DOTALL)
    matchesPattern = pattern.search(html_source.text)
    myDict=[]

    if matchesPattern:
        json_data = json.loads(matchesPattern.group(1))
        try:
            for items in json_data["results"]["explore"]["exploreCurated"]["tiles"]["items"]:
                appUrl=items["value"]["navLinks"][0]["url"]
                dummyDict={}
                dummyDict["appUrl"]=appUrl
                dummyDict["name"]=clean_string(items["value"]["title"])
                dummyDict["description"]=items["value"]["description"]
                dummyDict["imageUrl"]=items["value"]["imageURL"]
                dummyDict["id"]=appUrl.split("/")[-1][2:]
                myDict.append(dummyDict)
        except Exception as e:
            st.error("No matching app found")
    else:
        print("JSON data not found in the HTML file.")
    st.session_state.myDict=myDict 
    return gsheetThreader(countOfReviews,myDict)
