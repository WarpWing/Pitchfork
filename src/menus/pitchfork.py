import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

def send_email(subject, message_body, to_email, recipient_name):
    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')

    env = Environment(loader=FileSystemLoader('src\menus'))
    template = env.get_template('email_template.html')
    html_output = template.render(subject=subject, message_body=message_body, recipient_name=recipient_name)

    msg = MIMEText(html_output, 'html')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, [to_email], msg.as_string())
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

subject = "Test Subject"
message_body = "This is a test email sent from a Jinja2 template."

mail_list = [['chermsit@dickinson.edu', 'Ty Chermsirivatana'], ['wonge@dickinson.edu', 'Evan Wong']] #because who needs dicts?
#Execute Sending Function:
for i in range(len(mail_list)):
    print(f"Sending email to {mail_list[i][1]} at {mail_list[i][0]}...")