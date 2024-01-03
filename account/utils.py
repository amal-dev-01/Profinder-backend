

import pyotp
from django.utils import timezone


def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32())
    otp = totp.now()
    return otp





import random
import string
from django.conf import settings
from twilio.rest import Client  



def send_otp_phone(phone_number, otp):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=twilio_phone_number,
        to=phone_number
    )
    print(message,'mess')
    from twilio.base.exceptions import TwilioRestException

