from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud.dialogflow_v2 import types
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to DilSe Bot! The service is running 🚀'

DIALOGFLOW_PROJECT_ID = 'your-dialogflow-project-id'  # <-- Replace this
SESSION_ID = 'unique-session-id'  # Can use phone number for dynamic sessions
LANGUAGE_CODE = 'en'

@app.route('/sms', methods=['POST'])  # <-- Twilio sends POST to /sms
def sms_reply():
    incoming_msg = request.values.get('Body', '').strip()
    sender_number = request.values.get('From', '')  # for session_id

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, sender_number)

    text_input = types.TextInput(text=incoming_msg, language_code=LANGUAGE_CODE)
    query_input = types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    reply = response.query_result.fulfillment_text

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
