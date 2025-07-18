from twilio.rest import Client
from flask import current_app

def send_whatsapp_message(to_number: str, message_body: str) -> str:
    sid = current_app.config.get('TWILIO_ACCOUNT_SID')
    token = current_app.config.get('TWILIO_AUTH_TOKEN')
    from_num = current_app.config.get('TWILIO_WHATSAPP_NUMBER')

    if not all([sid, token, from_num]):
        raise ValueError("Twilio credentials are not fully configured.")

    if not to_number.startswith('+'):
        raise ValueError("Phone number must include country code (e.g., +966...).")
        
    try:
        client = Client(sid, token)
        message = client.messages.create(
            from_=from_num,
            body=message_body,
            to=f'whatsapp:{to_number}'
        )
        return message.sid
    except Exception as e:
        current_app.logger.error(f"An error occurred with Twilio API: {e}")
        raise