import smtplib
import os
import time
import requests
import csv
from datetime import datetime
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from typing_extensions import *

def find_week():
    return f"Meal for {datetime.now().strftime('%A, %B %d')}"

def get_menu_from_website():
    url = 'https://www.dickinson.edu/info/20205/campus_dining/4425/dining_menus'

    # Configure Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")  # Explicitly add headless argument
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    driver = webdriver.Chrome(options=options)  # Ensure the path to chromedriver is correctly set

    menu_data = ""

    try:
        driver.get(url)
        time.sleep(5)  # Adjust based on the page load time

        # Find all menu item elements for each meal type
        meals = ['Breakfast', 'Lunch', 'Dinner']
        for meal in meals:
            menu_data += f"Menu for {meal}:\n"
            xpath = f"//h3[contains(text(), '{meal}')]/following-sibling::div//li[@ng-repeat='item in category.ITEMS']"
            menu_items = driver.find_elements(By.XPATH, xpath)
            for item in menu_items:
                menu_data += item.text + "\n"  
            menu_data += "\n"

        # Get KOVE Menu
        menu_data += "Menu for KOVE:\n"
        kove_xpath = "//h2[contains(text(), 'KOVE')]/following-sibling::div//li[@ng-repeat='item in category.ITEMS']"
        kove_menu_items = driver.find_elements(By.XPATH, kove_xpath)
        for item in kove_menu_items:
            menu_data += item.text + "\n"  

    finally:
        driver.quit()

    return menu_data

def send_discord_webhook(menu_text): 
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']
    if not webhook_url:
        print("The webhook URL is not set. Please check your environment variables.")
        return

    sections = menu_text.split('\n\n')
    author = {
        "name": "Pitchfork Menu Bot",
        "url": "https://github.com/WarpWing/Pitchfork",
        "icon_url": "https://i.pinimg.com/originals/fa/ad/3e/faad3eac446d8a0933d010f383d2293f.png"
    }

    embed = {
        "author": author,
        "title": f"Meal for {datetime.now().strftime('%A, %B %d')}",  # Setting title to "{meal_type} for {current date}"
        "description": menu_text,
        "color": 3447003,
    }

    payload = {
        "username": "Pitchfork Menu Bot",
        "avatar_url": "https://i.pinimg.com/originals/fa/ad/3e/faad3eac446d8a0933d010f383d2293f.png",
        "embeds": [embed]
    }

    response = requests.post(webhook_url, json=payload)
    if response.status_code == 204:
        print(f"Webhook sent successfully for {datetime.now()}!")
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

mail_list = [['chermsit@dickinson.edu', 'Ty Chermsirivatana'], ['wonge@dickinson.edu', 'Evan Wong'],['kimbo@dickinson.edu','Boosung Kim'],['siripuns@dickinson.edu','Supasinee Siripun']]

def send_emails():
    menu_text = get_menu_from_website()
    for email, name in mail_list:
        print(f"Sending email to {name} at {email}...")
        send_email(find_week(), menu_text, email, name)

def send_test_emails():
    menu_text = get_menu_from_website()
    print(f"Sending email to {mail_list[0][1]} at {mail_list[0][0]}...")
    send_email(find_week(), menu_text, mail_list[0][0], mail_list[0][1])

#send_test_emails()
# Uncomment the next line to send to all emails
send_emails()

#Discord Webhook stuff
menu_text = get_menu_from_website()
send_discord_webhook(menu_text)
