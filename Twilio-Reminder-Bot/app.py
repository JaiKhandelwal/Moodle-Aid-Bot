import sys
import time
sys.path.append('../')

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from Lec2PDFScraper.scraper import lec_Scraper
from utils import send_response
import re
import emoji
app = Flask(__name__)


def another_fun(lec : str):
    url = lec_Scraper(lec)
    return url

@app.route("/")
def hello():
    return "Twillio Moodle Reminder II"


@app.route("/whatsapp", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    list_assignment = send_response()
    size = len(list_assignment)

    msg = request.form.get('Body')
    print(msg)

    reply_text = "I was Built for HackX by Scaler Academy"

    pattern_1 = "Remaining Assignments"
    pattern_2 = "Download PDF"
    BBURL = "https://lectures.iris.nitk.ac.in/playback/presentation/2.0/*"
    if re.match(pattern_1, msg,re.IGNORECASE) :
        reply = "Assignments Remaining : " + str(size)  + "\n" +"Type a Number Between 0 and " + \
            str(size-1) + ". Assignments are Arranged in Ascending Order of Submission Date"
        reply_x = MessagingResponse()
        reply_x.message(reply)
        print(reply)
        return str(reply_x)

    elif re.match(pattern_2, msg, re.IGNORECASE) :
        reply = "Please Enter the URL from BigBlueButton" + "\n" + \
            "The URL Should be of the format https://lectures.iris.nitk.ac.in/playback/presentation/2.0/*"

    elif re.match(BBURL, msg):
        media_response = MessagingResponse()
        msg_x = media_response.message()
        lecture_URL = lec_Scraper(msg)
        msg_x.media(lecture_URL)
        return str(media_response)
    
    elif msg.isnumeric():
        if 0 <= int(msg) <= size-1:
            reply = list_assignment[int(msg)]
            reply_x = MessagingResponse()
            reply_x.message(reply)
            print(reply)
            return str(reply_x)

        else :
            reply = "Please Enter a Number Between 0 and " + \
                str(size-1) + ". Assignments are Arranged in Ascending Order of Submission Date"
            reply_x = MessagingResponse()
            reply_x.message(reply)
            print(reply)
            return str(reply_x)

    else :
        reply = "Hello User " + emoji.emojize(":grinning_face_with_big_eyes:") + "\n" +  \
            "Welcome to *Moodle Aid Kit*. We are currently Providing the Following Services: " + "\n" + "1. Remaining Assignments" + "\n" + "2. Download PDF" + \
             "\n" + "3. Upcoming Tests/Quizzes" + "\n" + "......& Many More Under Development" + "\n" + "\n" + "Made With " +  emoji.emojize(":red_heart:") + " By *Team Mint Money*" + \
             "\n" + "\n" + "Built for HackX'21"   
        reply_text = MessagingResponse()
        reply_text.message(reply)
        return str(reply_text)
    
    reply_text = MessagingResponse()
    reply_text.message(reply)
    return str(reply_text)

    
if __name__ == "__main__":
    app.run(debug=True)
