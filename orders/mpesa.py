import requests
import base64
from datetime import datetime
from django.conf import settings

def get_access_token():

    url =  "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(
        url,
        auth=(
            settings.MPESA_CONSUMER_KEY,
            settings.MPESA_CONSUMER_SECRET
        )
    )


    if response.status_code != 200:
        raise Exception("Failed to get M-Pesa access token")

    data = response.json()
    
    return data["access_token"]

def generate_password():

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password_string = (
        settings.MPESA_SHORTCODE +
        settings.MPESA_PASSKEY +
        timestamp
    )

    password = base64.b64encode(
        password_string.encode()
    ).decode()

    return password , timestamp

def stk_push(phone_number, amount, account_reference):

    acces_token = get_access_token()

    password, timestamp = generate_password()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {acces_token}",
        "content-type": "application/json"
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA":phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": "Restaurant Order Payment",
    }

    response = requests.post(url, json=payload, headers=headers)