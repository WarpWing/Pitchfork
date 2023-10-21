import smtplib
import os
import json
from datetime import datetime
import csv
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def find_week():
    today = datetime.now()
    with open('src/schedule.csv', 'r') as csvfile:
        rows = list(csv.DictReader(csvfile))
        for i in range(len(rows)):
            start_date_str = rows[i]['Date']
            start_date = datetime.strptime(f"{today.year}/{start_date_str}", '%Y/%m/%d')
            if i < len(rows) - 1:
                end_date_str = rows[i + 1]['Date']
                end_date = datetime.strptime(f"{today.year}/{end_date_str}", '%Y/%m/%d')
            else:
                end_date = datetime(today.year + 1, 1, 1)
            if start_date <= today < end_date:
                return rows[i]['Week']
    return "Week not found"

def read_json_menu():
    
    current_week = find_week().replace(" ", "")
    current_day = datetime.now().strftime('%A')  

    with open(f"src/menus/{current_week}.json", "r", encoding='utf-8') as f:
        week_menu = json.load(f)[current_week]

    formatted_menu = ""

    for meal in ['Breakfast', 'Lunch', 'Dinner']:
        formatted_menu += f"{meal}:\n"
        day_menu = week_menu.get(meal, {}).get(current_day, {})
        
        for dish, description in day_menu.items():
            if isinstance(description, list):
                description = ', '.join(description)
            formatted_menu += f"  {dish}: {description}\n"

    return formatted_menu

def send_email(subject, message_body, to_email, recipient_name):
    gmail_user = os.getenv('GMAIL_USER')
    gmail_password = os.getenv('GMAIL_PASSWORD')
    
    if to_email == 'wonge@dickinson.edu':
        greeting = f"BING CHILLING {recipient_name}, BING CHILLING BING CHILLING BING CHILLING \n\n"
    else:
        greeting = f"Hello {recipient_name}! Here is the menu for {datetime.now().strftime('%A')}. Please make sure to check in person for dietary restrictions and special needs. \n\n"
    message_body = greeting + message_body


    msg = MIMEText(message_body, 'plain')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_email

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(gmail_user, [to_email], msg.as_string())
        smtp_server.close()
    except Exception as e:
        print(f"Failed to send email: {e}")

mail_list = [['chermsit@dickinson.edu', 'Ty Chermsirivatana'], ['wonge@dickinson.edu', 'Evan Wong'],['kimbo@dickinson.edu','Boosung Kim']]

def send_emails():
    menu_text = read_json_menu()
    for email, name in mail_list:
        print(f"Sending email to {name} at {email}...")
        send_email(find_week(), menu_text, email, name)

def send_test_emails():
    menu_text = read_json_menu()
    print(f"Sending email to {mail_list[0][1]} at {mail_list[0][0]}...")
    send_email(find_week(), menu_text, mail_list[0][0], mail_list[0][1])

#send_test_emails()
# Uncomment the next line to send to all emails
send_emails()
