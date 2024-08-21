from phi.workflow import Workflow, Task
from phi.assistant import Assistant
from phi.tools.email import EmailTools
import PyPDF2
import requests
from requests_ntlm import HttpNtlmAuth
import openai

# Configuration details
receiver_email = ""
sender_email = ""
sender_name = ""
sender_passkey = ""

# SharePoint credentials and URL
sharepoint_url = ""  # Replace with your SharePoint URL
username = ""  # Replace with your SharePoint username
password = ""  # Replace with your SharePoint password

# Function to get PDF content from SharePoint
def get_pdf_content_from_sharepoint():
    try:
        response = requests.get(sharepoint_url, auth=HttpNtlmAuth(username, password))
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Failed to get PDF content: {e}")
        return None

# Function to extract information from PDF content
def extract_info_from_pdf_content(pdf_content):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_content)
        full_text = ""
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                full_text += text
        return full_text
    except Exception as e:
        print(f"Failed to extract text from PDF content: {e}")
        return None

# Function to craft an email using OpenAI
def craft_email(subject, body, extracted_text):
    openai.api_key = ""  # Replace with your OpenAI API key
    prompt = f"{body}\n\n{extracted_text}\n\nRegards,\nMaha"
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Define SharePoint Assistant for fetching PDF
sharepoint_assistant = Assistant(
    tools=[
        get_pdf_content_from_sharepoint
    ]
)

# Define PDF Extraction Assistant
pdf_extractor_assistant = Assistant(
    tools=[
        extract_info_from_pdf_content
    ]
)

# Define Email Assistant for sending emails
email_assistant = Assistant(
    tools=[
        EmailTools(
            receiver_email=receiver_email,
            sender_email=sender_email,
            sender_name=sender_name,
            sender_passkey=sender_passkey,
        )
    ]
)

# Define subject and body variables
subject = "PDF Contents"
body = "Dear recipient,\n\nAttached please find the PDF info."

# Workflow for fetching PDF, extracting content, crafting email, and sending email
pdf_email_workflow = Workflow(
    name="PDF Email Workflow",
    tasks=[
        Task(
            description="Fetch PDF content from SharePoint",
            assistant=sharepoint_assistant,
            show_output=False,
        ),
        Task(
            description="Extract information from PDF content",
            assistant=pdf_extractor_assistant,
            show_output=False,
        ),
        Task(
            description="Craft email content using OpenAI",
            assistant=Assistant(
                tools=[
                    craft_email
                ]
            ),
            show_output=False,
            actions=[
                Assistant().print_response(f"craft_email('{subject}', '{body}', previous_task_result)")
            ]
        ),
        Task(
            description="Send email with crafted content",
            assistant=email_assistant,
            show_output=False,
            actions=[
                email_assistant.print_response(f"send an email with subject '{subject}' and body '{{previous_task_result}}'")
            ]
        ),
    ],
)

# Execute the workflow
pdf_email_workflow.print_response("Running the PDF Email Workflow", markdown=True)
