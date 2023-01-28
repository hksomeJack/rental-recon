import sqlalchemy as db
import smtplib, ssl, requests, time
from bs4 import BeautifulSoup
from sqlalchemy import Column, String, MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from selenium import webdriver


url = "https://<RENTAL.PLACE>/vacancies" # for requests/bs4
port = 465  # For SSL
password = "" # obviously not a great way to do this
headers= {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
webdriver_location=""


# Create a secure SSL context
context = ssl.create_default_context()

sender_email = "FILL THIS IN"
receiver_email1 = "FILL THIS IN""
receiver_email2 = "FILL THIS IN""
message1 = """\
Subject: Rental Listing Available

Listing detected. See it now: https://RENTAL.PLACE/vacancies."""

message2 = """\
Subject: Rental Listing Available

There is no listing. Sorry"""

def eMailSend(receiver_email, message):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

driver = webdriver.Chrome(webdriver_location)
driver.get(url)
time.sleep(2) # let JS load.
soup = BeautifulSoup(driver.page_source, features = "lxml")

# Determine if we're out of luck
noResultElem = soup.find_all(id='no-results')
if noResultElem == []:
    print('There is a listing')
    print(noResultElem)
    eMailSend(receiver_email1, message1)
    eMailSend(receiver_email2, message1)

else:
    print(noResultElem)
    eMailSend(receiver_email1, message2)
    eMailSend(receiver_email2, message2)
