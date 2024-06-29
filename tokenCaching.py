import json
import requests
import base64
from datetime import datetime, timedelta

def save_token(token_data):
    token_data['expires_at'] = (datetime.now() + timedelta(seconds=token_data['expires_in'])).isoformat()
    with open('token.json', 'w') as token_file:
        json.dump(token_data, token_file)

def load_token():
    try:
        with open('token.json', 'r') as token_file:
            token_data = json.load(token_file)
            token_data['expires_at'] = datetime.fromisoformat(token_data['expires_at'])
            return token_data
    except FileNotFoundError:
        return None

def is_token_valid(token_data):
    return datetime.now() < token_data['expires_at']

def get_new_token(CLIENT_ID,CLIENT_SECRET):

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    url = "https://api-m.paypal.com/v1/oauth2/token"
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    save_token(response.json())
    return response.json()['access_token']

def get_access_token(client_id, client_secret):
    token_data = load_token()
    if token_data and is_token_valid(token_data):
        return token_data['access_token']
    else:
        new_token_data = get_new_token(client_id, client_secret)
        return new_token_data

