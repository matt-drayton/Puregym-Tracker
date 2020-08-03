from settings import EMAIL, PIN, POLLING_RATE, ALERT_THRESHOLD, OPEN_TIME, CLOSE_TIME
import requests
from bs4 import BeautifulSoup
import time as time_
from win10toast import ToastNotifier
from datetime import datetime, time
import sys

LOGIN_URL = "https://www.puregym.com/login/"
API_LOGIN_URL = "https://www.puregym.com/api/members/login/"
URL = "https://www.puregym.com/members/"


# Payload sent when signing into puregym
login_payload = {"associateAccount":"false",
                "email":EMAIL,
                "pin":PIN}

def is_time_between(begin_time, end_time):
  '''
  Checks whether the gym is open, according to times set in settings
  '''
  check_time = datetime.now().time()
  if begin_time < end_time:
    return check_time >= begin_time and check_time <= end_time
  else: # crosses midnight
    return check_time >= begin_time or check_time <= end_time

def get_data():
  '''
  Finds how many people are in the gym currently
  '''
  with requests.Session() as s:
    # Get token for form submission
    initial = s.get(LOGIN_URL)
    soup = BeautifulSoup(initial.content, 'html.parser')

    token = soup.find('input', {'name': '__RequestVerificationToken'}).attrs['value']
    headers = {'__RequestVerificationToken': token}

    #Log into puregym
    s.post(API_LOGIN_URL, data=login_payload, headers=headers)

    # Get members page
    page = s.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Find HTML element containing number of people
    results = soup.find("span", class_='heading heading--level3 secondary-color margin-bottom')
    # If no such element exists, credentials were likely incorrect. Exit program.
    if results is None:
      print("Error, credentials are incorrect")
      sys.exit()

    # Find the count from the inner HTML of the element  
    count = int(results.text.split()[0])
    return count

def pause():
  # Will likely change to a lambda function
  time_.sleep(60*60)

if __name__ == '__main__':
  toaster = ToastNotifier()
  while True:
    # Is gym open?
    if is_time_between(time(OPEN_TIME, 0), time(CLOSE_TIME, 0)):
      print("Polling")
      count = get_data()
      
      if count < ALERT_THRESHOLD:
        print("Currently "+str(count)+" people in the gym. This is below threshold.")
        toaster.show_toast(title="Gym is available", 
                          msg="Currently "+str(count)+" people in the gym. This is below threshold. Click to mute for 1hr.", 
                          callback_on_click=pause)
      else:
        print("Currently "+str(count)+" people in the gym.")
      time_.sleep(POLLING_RATE)
    else:
      # If not between opening times, sleep for 10 mins
      time_.sleep(600)  
