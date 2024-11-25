from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from signalwire_swaig.core import SWAIG, SWAIGArgument
import requests
import base64

# Load environment variables
load_dotenv(override=True)

# Flask setup
app = Flask(__name__)
swaig = SWAIG(app, auth=(os.getenv('HTTP_USERNAME'), os.getenv('HTTP_PASSWORD')))

# Helper functions
def send_email(to_email, subject, body):
    url = f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages"
    auth = ("api", os.getenv("MAILGUN_API_KEY"))
    data = {"from": f"{os.getenv('MAILGUN_FROM_NAME')} <{os.getenv('MAILGUN_FROM_EMAIL')}>", "to": to_email, "subject": subject, "text": body}
    response = requests.post(url, auth=auth, data=data)
    return response.status_code, response.json()

def send_sms(phone_number, message):
    url = f"https://{os.getenv('SIGNALWIRE_SPACE')}.signalwire.com/api/laml/2010-04-01/Accounts/{os.getenv('PROJECT_ID')}/Messages.json"
    data = {"To": phone_number, "From": os.getenv("SIGNALWIRE_FROM_NUMBER"), "Body": message}
    credentials = f"{os.getenv('PROJECT_ID')}:{os.getenv('AUTH_TOKEN')}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }
    response = requests.post(url, data=data, headers=headers)
    return response.status_code, response.json()

def notify_slack(channel, message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {os.getenv('SLACK_BOT_TOKEN')}", "Content-Type": "application/json"}
    payload = {"channel": channel, "text": message}
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code, response.json()

# SWAIG endpoints
@swaig.endpoint("Send Email Notification",
    to_email=SWAIGArgument("string", "Recipient email address", required=True),
    subject=SWAIGArgument("string", "Email subject", required=True),
    body=SWAIGArgument("string", "Email body", required=True))
def send_email_notification(to_email, subject, body, meta_data_token, meta_data):
    status, response = send_email(to_email, subject, body)
    return f"Email sent with status {status}.", []

@swaig.endpoint("Send SMS Notification",
    phone_number=SWAIGArgument("string", "Recipient phone number", required=True),
    message=SWAIGArgument("string", "SMS message body", required=True))
def send_sms_notification(phone_number, message, meta_data_token, meta_data):
    status, response = send_sms(phone_number, message)
    return f"SMS sent with status {status}.", []

@swaig.endpoint("Notify Slack Channel",
    channel=SWAIGArgument("string", "Slack channel ID", required=True),
    message=SWAIGArgument("string", "Slack message body", required=True))
def notify_slack_channel(channel, message, meta_data_token, meta_data):
    status, response = notify_slack(channel, message)
    return f"Slack notification sent with status {status}.", []

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', 5000), debug=os.getenv('DEBUG'))
