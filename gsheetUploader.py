from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import json

my_dict={}
my_dict['type']=st.secrets['google_keys']['type']
my_dict['project_id']=st.secrets['google_keys']['project_id']
my_dict['private_key_id']=st.secrets['google_keys']['private_key_id']
my_dict['private_key']=st.secrets['google_keys']['private_key']
my_dict['client_email']=st.secrets['google_keys']['client_email']
my_dict['auth_uri']=st.secrets['google_keys']['auth_uri']
my_dict['client_id']=st.secrets['google_keys']['client_id']
my_dict['token_uri']=st.secrets['google_keys']['token_uri']
my_dict['auth_provider_x509_cert_url']=st.secrets['google_keys']['auth_provider_x509_cert_url']
my_dict['client_x509_cert_url']=st.secrets['google_keys']['client_x509_cert_url']
my_dict['universe_domain']=st.secrets['google_keys']['universe_domain']

scopes = ['https://www.googleapis.com/auth/spreadsheets']
scopeCreate = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(my_dict, scopes=scopes)
credentialCreate = service_account.Credentials.from_service_account_info(my_dict, scopes=scopeCreate)
service = build('sheets', 'v4', credentials=credentials)

def sheetWriter(spreadsheet_id,sheet_name,myDict):
    requests = []
    row1=['Product Name','Description','Image Url','Overall Rating','Total Downloads']
    row4=['Rating','Username','Review','Date']

    row2=[myDict['name'],myDict['description'],myDict['imageUrl'],myDict['overallRating'],myDict['totalDownloads']]

    service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range=f'{sheet_name}!A1:E1',  
    valueInputOption='RAW',
    body={'values': [row1]}
    ).execute()
    
    service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range=f'{sheet_name}!A4:D4',  
    valueInputOption='RAW',
    body={'values': [row4]}
    ).execute()
    
    service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id,
    range=f'{sheet_name}!A2:E2',  
    valueInputOption='RAW',
    body={'values': [row2]}
    ).execute()

def sheetMaker(spreadsheet_id,sheet_name,myDict):
    requests=[{
        'addSheet': {
            'properties': {
                'title': sheet_name
            }
        }
    }]

    request_body = {
        'requests': requests
    }

    response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=request_body).execute()
    sheetWriter(spreadsheet_id,sheet_name,myDict)

def create_google_sheet():
    service = build('sheets', 'v4', credentials=credentialCreate)
    drive_service = build('drive', 'v3', credentials=credentialCreate)
    spreadsheet = {
        'properties': {
            'title': 'New Google Sheet'
        }
    }
    
    spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
    spreadsheet_id = spreadsheet.get('spreadsheetId')
   
    try:
        permission = {'type': 'anyone',
                      'role': 'writer'}
        drive_service.permissions().create(fileId=spreadsheet_id,body=permission).execute()
    except Exception as error:
        return print('Error while setting permission:', error)
    return spreadsheet_id

def gsheetUpload(spreadsheet_id,myDict,j):
    sheetMaker(spreadsheet_id,j['name'],myDict)
    
    data = j['df']
    data['date'] = data['date'].astype(str)
    
    values = data.values.tolist()
    csv_file_name=j['name']
    
    service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=f'{csv_file_name}!A5:Z').execute()
    
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f'{csv_file_name}!A5',  
        valueInputOption='RAW',
        body={'values': values}
    ).execute()
