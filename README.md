[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwaipayan05/Assignment-Reminder-Moodle/issues)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/dwaipayan05/Assignment-Reminder-Moodle)

### Assignment Reminder Moodle
*Disclaimer* : The Project is highly susceptible to bugs as it is based on scraping data off the Moodle LMS. Since such websites are subject to change, certain modifications would have to be made to the program for making the Twilio Bot to scrape without any hinderance.

### About
A Twilio Whatsapp Bot which scrapes data from [Moodle NITK](https://courses.iris.nitk.ac.in/my/) which can be used to get information about remaining Assignments in your respective Department in NITK. This is a prototype, for the Twilio Bot to work the callback URL needs to be either exposed using `ngrok` to the web or hosted using a hosting service like heroku or netlify.

### Motivation
Didn't want to keep rechecking Moodle NITK to get an idea about upcoming assignments, instead, I preferred do it from the comfort of my smartphone

### Demo Video
You can find the link to the Demo Video [here](https://drive.google.com/file/d/1d3h4a9oGgzTGKbHto6meJSskTkGe3RI9/view?usp=sharing)

### Packages Used
- Selenium
- TwiML
- Flask
- ngrok

### How can you use this ?
- Create a Twilio Account and create a Whatsapp Sandbox Number
- Inside the folder [Date Scraper](./DateScraper) create a `.env` file with your credentials
  ```
     IRIS_USERNAME = ########
     IRIS_PASSWORD = ########
  ```
- Hopefully, you'd have hosted the Flask App on a Public Hosting Website
- Copy the URL to that Website with `<-------URL------>/whatsapp` as callback endpoint and paste it on Twilio's Console
- Now you can text the Whatsapp Number and get details about remaining assigments in your Moodle Account


Feel Free to Open Issues 💙
