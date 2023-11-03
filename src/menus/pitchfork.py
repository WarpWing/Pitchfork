import smtplib
import os
import json
import requests
from datetime import datetime
import csv
from email.mime.text import MIMEText


def find_week():
    today = datetime.now()
    with open(os.path.join('src', 'schedule.csv'), 'r') as csvfile:
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

    with open(os.path.join('src', 'menus', f'{current_week}.json'), "r", encoding='utf-8') as f:
        data = json.load(f)

    formatted_menu = ""

    if current_week in data:
        week_menu = data[current_week]

        formatted_menu += f"Breakfast:\n"
        breakfast_menu = week_menu.get('Breakfast', {}).get(current_day, {})
        for dish, description in breakfast_menu.items():
            if isinstance(description, list):
                description = ', '.join(description)
            formatted_menu += f"  {dish}: {description}\n"

        formatted_menu += "Lunch:\n"
        if current_week in ['Week2', 'Week3']:
            lunch_menu = data['Week2'][current_week].get(current_day, {})
        else:
            lunch_menu = week_menu.get('Lunch', {}).get(current_day, {})
        for dish, description in lunch_menu.items():
            if isinstance(description, list):
                description = ', '.join(description)
            formatted_menu += f"  {dish}: {description}\n"

        formatted_menu += f"Dinner:\n"
        dinner_menu = week_menu.get('Dinner', {}).get(current_day, {})
        for dish, description in dinner_menu.items():
            if isinstance(description, list):
                description = ', '.join(description)
            formatted_menu += f"  {dish}: {description}\n"
    else:
        for meal in ['Breakfast', 'Dinner']:
            formatted_menu += f"{meal}:\n"
            day_menu = data.get(meal, {}).get(current_day, {})
            for dish, description in day_menu.items():
                if isinstance(description, list):
                    description = ', '.join(description)
                formatted_menu += f"  {dish}: {description}\n"

        if 'Week2' in data and current_week in data['Week2']:
            formatted_menu += "Lunch:\n"
            lunch_menu = data['Week2'][current_week].get(current_day, {})
            for dish, description in lunch_menu.items():
                if isinstance(description, list):
                    description = ', '.join(description)
                formatted_menu += f"  {dish}: {description}\n"

    return formatted_menu



def send_discord_webhook(menu_text):
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    if not webhook_url:
        print("The webhook URL is not set. Please check your environment variables.")
        return

    sections = menu_text.split('\n\n')
    embeds = []
    author = {
        "name": "Pitchfork Menu Bot",
        "url": "https://github.com/WarpWing/Pitchfork",
        "icon_url": "https://i.pinimg.com/originals/fa/ad/3e/faad3eac446d8a0933d010f383d2293f.png"
    }

    for section in sections:
        meal_type, items = section.split(':\n', 1)
        fields = []
        for item in items.split('\n'):
            if item:
                if ': ' not in item:
                    continue
                dish, description = item.split(': ')
                fields.append({
                    "name": dish,
                    "value": description,
                    "inline": True
                })
        embed = {
            "author": author,
            "title": meal_type,
            "fields": fields,
            "color": 15258703,
        }
        embeds.append(embed)

    payload = {
        "username": "Pitchfork Menu Bot",
        "avatar_url": "https://i.pinimg.com/originals/fa/ad/3e/faad3eac446d8a0933d010f383d2293f.png",
        "content": f"Here is the menu for {datetime.now().strftime('%A')}",
        "embeds": embeds
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print("Webhook sent successfully!")
    else:
        print(f"Failed to send webhook with status code: {response.status_code}")


def send_email(subject, message_body, to_email, recipient_name):
    gmail_user = os.environ['GMAIL_USER']
    gmail_password = os.environ['GMAIL_PASSWORD']

    if to_email == 'wonge@dickinson.edu':
        greeting = f"BING CHILLING {recipient_name}, BING CHILLING BING CHILLING BING CHILLING \n\n"
    elif to_email == 'siripuns@dickinson.edu':
        greeting = f"IM SUPASHY SUPASHY {recipient_name}, BUT WAIT A MINUTE WHILE I MAKE YOU MINE MAKE YOU MINEE IM SUPASHYYYYYYYYYYYYYYYYYYYYY \n\n"
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

mail_list = [['chermsit@dickinson.edu', 'Ty Chermsirivatana'], ['wonge@dickinson.edu', 'Evan Wong'],['kimbo@dickinson.edu','Boosung Kim'],['siripuns@dickinson.edu','Supasinee Siripun'],['gonzalec@dickinson.edu','Chris Gonzalez']]

def send_emails():
    menu_text = read_json_menu()
    for email, name in mail_list:
        print(f"Sending email to {name} at {email}...")
        send_email(find_week(), menu_text, email, name)

def send_test_emails():
    menu_text = read_json_menu()
    print(f"Sending email to {mail_list[0][1]} at {mail_list[0][0]}...")
    send_email(find_week(), menu_text, mail_list[0][0], mail_list[0][1])

send_test_emails()
# Uncomment the next line to send to all emails
#send_emails()

#Discord Webhook stuff
#menu_text = read_json_menu()
#send_discord_webhook(menu_text)
