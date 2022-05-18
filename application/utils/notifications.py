from twilio.rest import Client

def send_notification(phone_number, pdf=""):
    
    # Api Tokens
    account_sid = 'AC30f1f813921dd06d762d928485ee4528' 
    auth_token = '9b556121018e0e825d378400e775759e' 

    # Creates a client that will send the message
    client = Client(account_sid, auth_token) 
    
    text = 'Test'

    # Sends the message 
    message = client.messages.create(   
                                messaging_service_sid='MGf0c5a4ab7ddc5a2018fa730f6d7cb029',
                                body=text,      
                                to=phone_number,
                            )
    
    print("Text message has been send to: %s" % phone_number)
