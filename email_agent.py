import os
from dotenv import load_dotenv
from typing import Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agents import Agent, function_tool

load_dotenv(override=True)
MY_EMAIL = "naomiarchieves2@gmail.com"
MY_PW = os.getenv("SMTP_PW")

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    msg = MIMEMultipart()
    msg['From'] = MY_EMAIL
    msg['To'] = "rbpalmiano@gmail.com"
    msg['Subject'] = subject
    content = html_body
    msg.attach(MIMEText(content, 'text/html', 'utf-8'))
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PW)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs="rbpalmiano@gmail.com", msg=msg.as_string())
        return {"status": "success"}
    except:
        return {"status": "error"}


INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_html_email],
    model="gpt-4o-mini",
)
