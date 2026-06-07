from twilio.rest import Client

ACCOUNT_SID = "AC62614bd733d1ce10a9b1b3e058c4f9f6"
AUTH_TOKEN = "2ff6c444d40a4176d32e80ccf1a488a4"
MSG_SERVICE_SID = "MG2a5d4c13935363294d6ca6537123d94e"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_alert_sms(phone, message):
    print("SMS Function Called")
    print(phone)
    print(message)

    msg = client.messages.create(
        messaging_service_sid=MSG_SERVICE_SID,
        body=message,
        to=phone
    )
    return msg.sid

