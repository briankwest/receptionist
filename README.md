### README.md

# Receptionist AI Agent

## Overview

The **Receptionist AI Agent** is a virtual assistant designed to collect caller information and facilitate communication via Slack, SMS, and email. It uses the SignalWire SWAIG framework for centralized API functionality. This agent enhances productivity by notifying relevant team members through integrated communication tools.

---

## Features

1. **Information Collection**:
   - Collect and confirm caller's name, contact number, and reason for the call.
2. **Slack Notifications**:
   - Send caller information to a designated Slack channel.
3. **SMS Communication**:
   - Send SMS messages to callers with call details or instructions.
4. **Email Handling**:
   - Send email notifications via Mailgun.

---

## SWAIG Functions

### Base Endpoint: `/swaig`
- **Method**: POST
- **Content-Type**: `application/json`
- **Authentication**: Basic Auth (username/password from `.env`).

### 1. `send_email_notification`
**Description**: Sends an email notification using Mailgun.

- **Parameters**:
  ````json
  {
    "type": "object",
    "properties": {
      "to_email": {
        "type": "string",
        "description": "Recipient email address."
      },
      "subject": {
        "type": "string",
        "description": "Email subject."
      },
      "body": {
        "type": "string",
        "description": "Email body."
      }
    },
    "required": ["to_email", "subject", "body"]
  }
  ````

### 2. `send_sms_notification`
**Description**: Sends an SMS message to a caller.

- **Parameters**:
  ````json
  {
    "type": "object",
    "properties": {
      "phone_number": {
        "type": "string",
        "description": "Recipient phone number in E.164 format."
      },
      "message": {
        "type": "string",
        "description": "SMS message body."
      }
    },
    "required": ["phone_number", "message"]
  }
  ````

### 3. `notify_slack_channel`
**Description**: Sends a message to a specified Slack channel.

- **Parameters**:
  ````json
  {
    "type": "object",
    "properties": {
      "channel": {
        "type": "string",
        "description": "Slack channel ID where the message will be posted."
      },
      "message": {
        "type": "string",
        "description": "Slack message body."
      }
    },
    "required": ["channel", "message"]
  }
  ````

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd receptionist-ai
   ```

2. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` File**:
   Add the following environment variables:
   ```plaintext
   HTTP_USERNAME=<basic-auth-username>
   HTTP_PASSWORD=<basic-auth-password>
   SLACK_BOT_TOKEN=<slack-bot-token>
   SLACK_CHANNEL_ID=<slack-channel-id>
   MAILGUN_API_KEY=<mailgun-api-key>
   MAILGUN_DOMAIN=<mailgun-domain>
   MAILGUN_FROM_NAME=<sender-name>
   MAILGUN_FROM_EMAIL=<sender-email>
   SIGNALWIRE_API_KEY=<signalwire-api-key>
   SIGNALWIRE_SPACE=<signalwire-space>
   SIGNALWIRE_FROM_NUMBER=<signalwire-phone-number>
   PROJECT_ID=<signalwire-project-id>
   AUTH_TOKEN=<signalwire-auth-token>
   PORT=5000
   DEBUG=True
   ```

5. **Run the Application**:
   ```bash
   python app.py
   ```

---

## Usage

### Example API Request
Send a POST request to `/swaig` with the required parameters for the desired function.

#### Sample Request for `send_email_notification`
```json
{
  "function": "send_email_notification",
  "argument": {
    "to_email": "recipient@example.com",
    "subject": "Test Email",
    "body": "This is a test email from the Receptionist AI Agent."
  }
}
```

#### Sample Request for `send_sms_notification`
```json
{
  "function": "send_sms_notification",
  "argument": {
    "phone_number": "+1234567890",
    "message": "Hello, this is a test message from Receptionist AI Agent."
  }
}
```

#### Sample Request for `notify_slack_channel`
```json
{
  "function": "notify_slack_channel",
  "argument": {
    "channel": "C01ABCDEFG",
    "message": "New call received from +1234567890. Reason: General inquiry."
  }
}
```

---

## Notes

- Ensure the `.env` file is correctly configured with valid credentials.
- Use the provided SWAIG functions for seamless integration with email, SMS, and Slack services.

---

## Future Enhancements

1. **Call Transcription**: Add support for automatic transcription of calls.
2. **Extended Email Functionality**: Allow file attachments in email notifications.
3. **Analytics**: Integrate with analytics services for tracking call statistics.


