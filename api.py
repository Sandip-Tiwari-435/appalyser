import requests
from tokenCaching import get_access_token
import uuid
import streamlit as st

CLIENT_ID_UAT=st.secrets['paypal']['CLIENT_ID_UAT']
CLIENT_SECRET_UAT=st.secrets['paypal']['CLIENT_SECRET_UAT']
CLIENT_ID=st.secrets['paypal']['CLIENT_ID']
CLIENT_SECRET=st.secrets['paypal']['CLIENT_SECRET']
uuuid=uuid.uuid4()

def validatePayment(uid):
    if 'payments' in detailApi(uid)[0]:
        return False
    if confirmApi(uid)=='COMPLETED':
        return True

def confirmApi(uid):
    token=get_access_token(CLIENT_ID,CLIENT_SECRET)
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id':f'{uuid.uuid4()}',
        'Authorization': f'Bearer {token}',
    }
    try:
        response = requests.post(f'https://api-m.paypal.com/v2/checkout/orders/{uid}/capture', headers=headers, data='')
        return response.json()['status']
    except requests.exceptions.HTTPError as http_err:
        print(f'Http error {http_err}')

def detailApi(uid):
    token=get_access_token(CLIENT_ID,CLIENT_SECRET)
    headers = {
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f'https://api-m.paypal.com/v2/checkout/orders/{uid}', headers=headers, data='')
    return response.json()['purchase_units']

def mainApi(new_username,new_password,new_email):
    token=get_access_token(CLIENT_ID,CLIENT_SECRET)
    headers = {
        'Content-Type': 'application/json',
        'PayPal-Request-Id': f'{uuid.uuid4()}',
        'Authorization': f'Bearer {token}',
    }

    data = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "09f80740-38f0-11e8-b467-0ed5f89f718b", "amount": { "currency_code": "USD", "value": "20.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "user_action": "PAY_NOW", "return_url": "https://appalyser.streamlit.app/Home?username='+new_username+'&password='+new_password+ '&email='+new_email + '", "cancel_url": "https://appalyser.streamlit.app/Sign_In" } } } }'
    
    response = requests.post('https://api-m.paypal.com/v2/checkout/orders', headers=headers, data=data)
    return response.json()['links'][1]['href']

#detailApi('4R581954CR3074728')
