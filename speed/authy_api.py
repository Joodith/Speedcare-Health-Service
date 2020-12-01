from django.conf import settings
import requests

def send_verfication_code(user):
    data = {
    'api_key': settings.AUTHY_KEY,
    'via': 'sms',
    'country_code': user.country_code,
    'phone_number': user.phone_number,
    }
    url = 'https://api.authy.com/protected/json/phones/verification/start'
    response = requests.post(url,data=data)
    return response

def verify_sent_code(one_time_password, user):
    data= {
    'api_key': settings.AUTHY_KEY,
    'phone_number': user.phone_number,
    'country_code': user.country_code,
    'verification_code': one_time_password,
    }

    url = 'https://api.authy.com/protected/json/phones/verification/check'
    response = requests.get(url,data=data)
    return response
