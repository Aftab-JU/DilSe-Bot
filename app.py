
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google.cloud import dialogflow_v2 as dialogflow


app = Flask(__name__)

DIALOGFLOW_PROJECT_ID = 'your-dialogflow-project-id'
SESSION_ID = 'current-user-session'
LANGUAGE_CODE = 'en'

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

    text_input = dialogflow.types.TextInput(text=incoming_msg, language_code=LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)

    reply = response.query_result.fulfillment_text

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(reply)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
