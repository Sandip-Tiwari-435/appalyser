import requests
from tokenCaching import get_access_token
import uuid

CLIENT_ID_UAT = 'AQu1LL-aOtJRNLdz9qbl_RGkH5Ztmss1ny3X2--JvUpGoggcgsJ0U60pIWwIclqDd3xUBlWuiR2Pda3S'
CLIENT_SECRET_UAT = 'EBaTSLNMgDtp7QvIg6SQdhsEvH9DLqjFVMBu0rt2vLwTpJ5DyFh1uULvvQiar2Rww6o7P53PVVYr1CWo'
CLIENT_ID='Ac-P7tITyH9b0QAt-9TMpxfquLlf8Xo4b4wqILFCo6h_lizMNs-OTYBQbmcXSq4eYX3p1NXvYiSrMIDx'
CLIENT_SECRET='EK29Qc9D0vym1e1ZpnVKNcaBiDHV2EMEmZiH6QSxYa17_ghthK-xBuXYD8AH4qF3ADvyzq5AOXb8KAz0'
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

    data = '{ "intent": "CAPTURE", "purchase_units": [ { "reference_id": "09f80740-38f0-11e8-b467-0ed5f89f718b", "amount": { "currency_code": "USD", "value": "20.00" } } ], "payment_source": { "paypal": { "experience_context": { "payment_method_preference": "IMMEDIATE_PAYMENT_REQUIRED", "brand_name": "EXAMPLE INC", "locale": "en-US", "landing_page": "LOGIN", "user_action": "PAY_NOW", "return_url": "http://192.168.1.60:8501/Home?username='+new_username+'&password='+new_password+ '&email='+new_email + '", "cancel_url": "http://192.168.1.60:8501/Sign_In" } } } }'
    
    response = requests.post('https://api-m.paypal.com/v2/checkout/orders', headers=headers, data=data)
    return response.json()['links'][1]['href']

#detailApi('4R581954CR3074728')
