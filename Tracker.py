
import smtplib
from getpass import getpass
from bs4 import BeautifulSoup
import requests

import time
from datetime import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


## Step 1 : Get user and product details.
## Step 2 : Check price periodically
## Step 3 : If price reduced by certain percentage send email   

def sendEmail(data,price):
    '''
    paramter : data containing user data
    '''
    sender_email = "rimsha.maredia@gmail.com"
    recipient_email = data["email"]
    subject = "Price drop for" + data["title"]
    message = "Hello the price for " + data["title"]+ " has dropped to "+ str(price)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, "plain"))

    smtp_server = "smtp.gmail.com"  # Use the SMTP server of your email provider
    smtp_port = 587  # The port may vary depending on your provider


    # Create an SMTP object and establish a connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()  # Use TLS (Transport Layer Security) for encryption
    server.ehlo()
    server.login(sender_email, "ismm pcrx ygqi wmcn")  # Replace with your email password

    # Send the email
    text = msg.as_string()
    server.sendmail(sender_email, recipient_email, text)

    # Close the SMTP server connection
    server.quit()


def checkPrice(data):
    
    """
    Checks the current price and sends email if it has dropped by percentage provided by the user
    Parameters : data - dict of user data
    
    """
    
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})
    URL = data["URL"]
    print(URL)
    webpage = requests.get(URL,headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    
    
    data["title"] = soup.find("span",attrs={"id":'productTitle'}).text.strip()
    
    price = float(soup.find("span", attrs={"class":'a-price'}).find("span", attrs={"class" : "a-price-whole"}).text.strip() + soup.find("span", attrs={"class":'a-price'}).find("span", attrs={"class" : "a-price-fraction"}).text.strip())
    print("Current price : " + str(price))
    
    if(data["prevprice"] == None):
        data["prevprice"] = price
    else : 
        if((price - data["prevprice"])*100/data["prevprice"] >= data["drop-percent"]):
            sendEmail(data,price)
            
def inputDetails():
    '''
    returns dictionary containing user data
    '''
    data_dict = {}
    data_dict["prevprice"] = None
    data_dict["URL"] = input("\nEnter product URL:\n")
    disc = ""
    while(True):
        try:
            disc = float(input("\nEnter the discount % required: "))
            break
        except:
            pass
    data_dict["drop-percent"] = float(disc)
    data_dict["often"] = float(
        input("\nEnter (in secs.) how often you'd like to check the price: "))
    data_dict["email"] = input("\nEnter your Gmail ID: ")
    
    print(data_dict)
    return data_dict

        
def getTime(t):
    '''
    returns a string after converting time in seconds to hours/sec/min
    '''
    if t >= 3600:
        s = str(round(t // (3600), 2)) + " hours.\n"
    elif t >= 60:
        s = str(t // 60) + " mins, " + str(t % 60) + " secs.\n"
    else:
        s = str(t) + " secs.\n"
    return s