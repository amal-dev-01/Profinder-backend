from twilio.rest import Client
from django.conf import settings
from twilio.base.exceptions import TwilioRestException

client = Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
def send_sms(phone_number):
    try: 
        verification = client.verify \
                        .v2 \
                        .services(settings.SERVICE_SID) \
                        .verifications \
                        .create(to=phone_number, channel='sms')
        print(verification.sid)
        return verification.sid
    except TwilioRestException as e:
        print(e)
        return 
       

def verify_user_code(verification_sid, user_input):
    try:
        verification_check = client.verify \
        .v2 \
        .services(settings.SERVICE_SID) \
        .verification_checks\
        .create(verification_sid=verification_sid, code=user_input)
        return verification_check
    except:
        return