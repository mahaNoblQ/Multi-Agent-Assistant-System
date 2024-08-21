# PDF Email Workflow

This project automates the process of retrieving a PDF file from SharePoint, extracting its content, generating an email using OpenAI's GPT-4 model, and sending the email with the extracted content. The workflow is built using the `phi` framework.

# Requirements

Before running the script, ensure you have the following dependencies installed:

- Python 3.10+
- requests
- requests_ntlm
- PyPDF2
- openai
- phi

# Personal Info

You need to configure the script with your personal credentials and SharePoint details

receiver_email = "recipient@example.com"
sender_email = "sender@example.com"
sender_name = "Sender Name"
sender_passkey = "your-email-passkey"
sharepoint_url = "https://your-sharepoint-url"
username = "your-sharepoint-username"
password = "your-sharepoint-password"
openai.api_key = "your-openai-api-key"
