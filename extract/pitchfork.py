import requests
import os
import csv
import re
from bs4 import BeautifulSoup, Comment

def download_and_clean_file(url, filename):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Remove style tags
    for style in soup.find_all("style"):
        style.extract()

    for style in soup.find_all("col"):
        style.extract()
    
    # Remove comments
    for comment in soup.findAll(text=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove images
    for img in soup.find_all("img"):
        img.extract()

    # Remove elements with CSS properties and encoded image data
    for tag in soup.find_all():
        if tag.has_attr('style'):
            pass
        elif tag.has_attr('o:gfxdata') or tag.has_attr('v:imagedata'):
            tag.extract()

    with open(filename, 'w', encoding="utf-8") as f:
        f.write(str(soup))

csv_path = "extract\schedule.csv"

for i in range(1, 5):
    os.makedirs(f"Week {i}", exist_ok=True)

with open(csv_path, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader) 
    
    for row in reader:
        date, week, breakfast_url, lunch_url, dinner_url = row
        base_name = date.replace("/", "-")
        download_and_clean_file(breakfast_url, os.path.join(week, f"{base_name}_breakfast.html"))
        download_and_clean_file(lunch_url, os.path.join(week, f"{base_name}_lunch.html"))
        download_and_clean_file(dinner_url, os.path.join(week, f"{base_name}_dinner.html"))

print("Download, cleanup, and sorting complete!")
