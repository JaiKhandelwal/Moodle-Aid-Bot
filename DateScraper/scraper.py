import logging
import selenium
import time
import os
import re
import json
import shutil
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from decouple import config
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

IRIS_USERNAME = config('IRIS_USERNAME')
IRIS_PASSWORD = config('IRIS_PASSWORD')

PATH = "E:\Projects\Personal\Assignment Reminder Moodle\DateScraper\ChromeWeb Driver\chromedriver_win32\chromedriver.exe"

#Run in Headless Mode
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get("https://courses.iris.nitk.ac.in/calendar/view.php?view=month")
d = str(datetime.datetime.now())

def monthToNum(Month):
    return {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'Septemper': 9,
        'October': 10,
        'November': 11,
        'Decemeber': 12
    }[Month]


def timeConversion(s):
   if s[-2:] == "AM":
      if s[:2] == '12':
          a = str('00' + s[2:8])
      else:
          a = s[:-2]
   else:
      if s[:2] == '12':
          a = s[:-2]
      else:
          a = str(int(s[:2]) + 12) + s[2:8]
   return a

def parse_date(due_date):
    split_day = list(map(str, due_date.split(",")))
    date = split_day[1]
    split_date = list(map(str,date.split(" ")))
    day = int(split_date[1])
    month = monthToNum(split_date[2])
    year = int(split_date[3])

    parsed_date = [day, month, year]
    return parsed_date

def parse_time(due_date):
    split_day = list(map(str, due_date.split(",")))

    time = split_day[2]
    split_time = list(map(str,time.split(" ")))

    hr_min = split_time[1]
    hr_min_split = list(map(str,hr_min.split(":")))

    if len(hr_min_split[0]) == 1:
        hr_min = "0"+hr_min_split[0] + ":"  + hr_min_split[1]

    am_pm = split_time[2]
    time_12 = hr_min + ":00" + am_pm
    time_24 = timeConversion(s = time_12)

    return time_24
    
def dump_to_json(assignments):
    print("[" + d + "] : " + "Dumping to .JSON")
    filename = "Assignment.json"
    with open(filename, 'w') as output :
        json.dump(assignments, output, indent = 4)
    src = 'E:/Projects/Personal/Assignment Reminder Moodle/DateScraper/Assignment.json'
    dst = 'E:/Projects/Personal/Assignment Reminder Moodle/Twilio-Reminder-Bot'
    dest = os.path.join(dst,filename)
    shutil.move(src, dest)

def login():
    print("[" + d + "] : " + "Logging In Into Moodle")
    username = driver.find_element_by_id("user_login")
    username.send_keys(IRIS_USERNAME)

    password = driver.find_element_by_id("user_password")
    password.send_keys(IRIS_PASSWORD)

    loginbutton = driver.find_element_by_xpath("/html/body/div/div/div/div/div[2]/div/form/div/div[4]/div[2]/div/button")
    loginbutton.click()

def fetch_due_dates():
    urls = []
    print("[" + d + "] : " + "Fetching Due Dates")
    prev_month = driver.execute_script("""
        var link = document.getElementsByClassName("arrow_link previous")[0].href;
        return link;
    """)
    next_month = driver.execute_script("""
        var link = document.getElementsByClassName("arrow_link next")[0].href;
        return link;
    """)

    months = [prev_month, next_month]

    url_curr = driver.execute_script("""
        var NodeList = document.querySelectorAll("[data-action = 'view-event']");
        url_vec = [];
        for (var i = 0; i<NodeList.length ; i++)
        {
            url_vec.push(NodeList[i].href);
        }
        return url_vec;
    """
    )
    urls.extend(url_curr)
    for month in months :
        driver.get(month)
        url_x = driver.execute_script("""
        var NodeList = document.querySelectorAll("[data-action = 'view-event']");
        url_vec = [];
        for (var i = 0; i<NodeList.length ; i++)
        {
            url_vec.push(NodeList[i].href);
        }
        return url_vec;
    """
        )
        urls.extend(url_x)

    assignments = []
    print("[" + d + "] : " +
          "Merging Assignment Dictionary")
    for url in urls:
        pattern = 'https://courses.iris.nitk.ac.in/mod/assign/*'

        if re.match(pattern, url):
        
            driver.get(url)
            due_date = driver.execute_script("""
                due_date = document.getElementsByClassName("cell c1 lastcol")[2].innerHTML
                return due_date
            """)

            
            assignment_dict = dict()
            assignment_dict["Date"] = parse_date(due_date)
            assignment_dict["Time"] = parse_time(due_date)
            assignment_dict["Title"] = driver.title
            assignments.append(assignment_dict)
            
    dump_to_json(assignments)

        
    
def run_scraper():
    login()
    fetch_due_dates()
    print("[" + d + "] : " + "Closing Web Driver")
    driver.close()


if __name__ == "__main__":
    run_scraper()
