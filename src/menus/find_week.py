from datetime import datetime
import csv

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

print(find_week())
