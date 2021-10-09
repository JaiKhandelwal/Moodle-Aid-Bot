import logging
import cloudinary
import selenium
import time
import os
import re
import sys
import shutil
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from cloudinary.uploader import upload

from decouple import config
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests

IRIS_USERNAME = config('IRIS_USERNAME')
IRIS_PASSWORD = config('IRIS_PASSWORD')

cloudinary.config(cloud_name=config('CLOUD_NAME'), api_key=config(
    'API_KEY'), api_secret=config('API_SECRET'))

PATH = "E:\Projects\Personal\Assignment Reminder Moodle\DateScraper\ChromeWeb Driver\chromedriver_win32\chromedriver.exe"

#Run in Headless Mode
chrome_options = Options()
chrome_options.add_extension(
    'E:\Projects\Personal\Assignment Reminder Moodle\Console Importer\console_importer.crx')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
prefs = {"download.default_directory": "E:\Projects\Personal\Assignment Reminder Moodle\Lec2PDFScraper\Downloaded_PDF"}
chrome_options.add_experimental_option("prefs", prefs)
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(PATH, options=chrome_options)
driver.get("https://courses.iris.nitk.ac.in/my/")

def initialize_driver(bigblue_Button):
    clean_dir()
    driver.get(bigblue_Button)
    try:
        time.sleep(10)
        w = WebDriverWait(driver, 15)
        w.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "acorn-fullscreen-button")))

        print("[" + datetime.now() + "] : " + "Page Loaded")
    except :
        print("Timeout happened no page load")


def download_pdf():
    driver.execute_script(
        "$i('https://cdnjs.cloudflare.com/ajax/libs/jspdf/1.3.2/jspdf.min.js')")
    time.sleep(2)
    print("[" + datetime.now() + "] : " + "JSPDF Imported")
    lecturetitle = driver.execute_script("""
    var lecturetitle = document.getElementById('recording-title').innerHTML;
        var thumbnail = document.getElementsByClassName('thumbnail-wrapper');
        var imageUrls = new Array();
        var x = 0;

        var dict = [];

        var maxheight = 0;
        var maxwidth = 0;

        for (var i = 0; i < thumbnail.length; i++) {
        
        var thumbnailDiv = thumbnail[i];
        var image = thumbnailDiv.getElementsByTagName("img")[0];
        var imgname = image.src.replace(/^.*[\\\/]/, '');
        var source = image.src;
        
        var curr_ht = image.naturalHeight;
        var curr_wd = image.naturalWidth;
        
        
    
        if(!(imgname in dict))
        {           
            imageUrls[x] = source;
            dict[imgname] = source;
            x++;    
        }

        maxheight = Math.max(maxheight, curr_ht);
        maxwidth = Math.max(maxwidth, curr_wd);

    }

        console.log(dict);
        function pix2mm(val){
            return (val*0.2645833333);
        }
        async function savePdf() {
            const multiPng = await generatePdf(imageUrls);
            multiPng.save(lecturetitle);
        }

        async function addImageProcess(src) {
            return new Promise((resolve, reject) => {
                let img = new Image();
                img.src = src;
                img.onload = () => resolve(img);
                img.onerror = reject;
            
            });
        }
        
        async function generatePdf(imageUrls) {
            var orientation;
            if(maxwidth >= maxheight)
            {
                orientation = 'landscape';
            }

            else if ( maxwidth < maxheight)
            {
                orientation = 'portrait'
            }

            var width_mm = pix2mm(maxwidth);
            var height_mm = pix2mm(maxwidth);
            const doc = new jsPDF(orientation, 'mm', [width_mm, height_mm], true);
            

            for (const [i, url] of imageUrls.entries()) {
                const image = await addImageProcess(url);
                var filename = image.src.replace(/^.*[\\\/]/, '');
                console.log("Fetching " + filename);
                img_ht = pix2mm(image.naturalHeight);
                img_wt = pix2mm(image.naturalWidth);
                doc.addImage(image, "png", 0, 0, img_wt, img_ht, null, 'FAST' );
                if (i !== imageUrls.length - 1) {
                    doc.addPage();
                }
            }
            return doc;
        }
        
        savePdf().then(console.log("PDF Saved"));
        return lecturetitle
    """)
    time.sleep(10)
    print("[" + datetime.now() + "] : " + "Downloaded " + lecturetitle + ".pdf")


def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath) 

    return file_paths

def upload_cloud():
    filepath = []
    while(len(filepath) < 1):
        filepath = get_filepaths(
        'E:/Projects/Personal/Assignment Reminder Moodle/Lec2PDFScraper/Downloaded_PDF')
   
    upload_res = cloudinary.uploader.upload(filepath[0])
    print("[" + datetime.now() + "] : " +
          "Cloudinary URL Generated : " + upload_res['url'])
    return upload_res['url']

def clean_dir():
    dir = 'E:/Projects/Personal/Assignment Reminder Moodle/Lec2PDFScraper/Downloaded_PDF'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def login():
    print("[" + datetime.now() + "] : " + "Logging In Into Moodle")
    
    username = driver.find_element_by_id("user_login")
    username.send_keys(IRIS_USERNAME)

    password = driver.find_element_by_id("user_password")
    password.send_keys(IRIS_PASSWORD)

    loginbutton = driver.find_element_by_xpath(
        "/html/body/div/div/div/div/div[2]/div/form/div/div[4]/div[2]/div/button")
    loginbutton.click()

def lec_Scraper(lecture_URL):
    login()
    initialize_driver(lecture_URL)
    download_pdf()
    return upload_cloud()

if __name__ == "__main__":
    print(lec_Scraper(sys.argv[0]))
