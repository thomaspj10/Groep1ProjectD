from twilio.rest import Client
from utils.settings import read_settings

def send_notification(phone_number, message, pdf=""):
    
    # Reads the settings
    settings = read_settings()

    # Api Tokens from the settings
    account_sid = settings["sms_credentials"]["account_sid"]
    auth_token = settings["sms_credentials"]["auth_token"] 
    messaging_service = settings["sms_credentials"]["messaging_service_sid"]

    # Creates a client that will send the message
    client = Client(account_sid, auth_token) 
    
    text = message

    # Sends the message 
    message = client.messages.create(   
                                messaging_service_sid=messaging_service,
                                body=text,      
                                to=phone_number,
                            )
    
    print("Text message has been send to: %s" % phone_number)
