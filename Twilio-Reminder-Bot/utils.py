import sys
sys.path.append('../')

import json
import datetime
from DateScraper.scraper import run_scraper

# run_scraper()

def find_remaining_time(date, time):
    split_time = list(map(str, time.split(":")))
    hours = int(split_time[0])
    minutes = int(split_time[1])
    seconds = int(split_time[2])

    current_time = datetime.datetime.now()
    due_date = datetime.datetime(date[2], date[1], date[0], hours, minutes, seconds, 0)
    remaining_time = due_date - current_time
    if current_time < due_date:
        return remaining_time
    else :
        return -1

def reminder(time_left, title):
    current_time = datetime.datetime.now()
    message_header = "*REMINDER*" + "\n"
    message_title = "Assignment Title : {assignment_name}".format(assignment_name = title) + "\n"
    message_time = "Time Remaining : {time_remaining}".format(time_remaining = time_left) + "\n"
    message_end = "Last Updated On : {date}".format(date = current_time) + "\n"
    return message_header + message_title + message_time + message_end

def send_response():
    with open('./Assignment.json') as json_dump:
        assignment_data = json.load(json_dump)

    reminders = []
    for assgn in assignment_data:
        date = assgn['Date']
        time = assgn['Time']
        title = assgn['Title']
        time_left = find_remaining_time(date, time)
        
        if time_left == -1:
            continue
        else :
            rem = reminder(time_left, title)
            reminders.append(rem)
    
    return reminders
            

if __name__ == "__main__":
    send_response()
