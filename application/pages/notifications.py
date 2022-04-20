from twilio.rest import Client

def send_notification():
    from twilio.rest import Client 
    
    account_sid = 'ACf1a8a3ce82a894972f2ec247038279d6' 
    auth_token = '8c43f388fd655fad1e3f810b5a431b15' 
    client = Client(account_sid, auth_token) 
    
    text = 'Test'
    phonenumber = ''
    message = client.messages.create(   
                                messaging_service_sid='MGf0c5a4ab7ddc5a2018fa730f6d7cb029',
                                body=text,      
                                to=phonenumber,
                            )

send_notification()