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


login_payload = {"associateAccount":"false",
                "email":EMAIL,
                "pin":PIN}

def is_time_between(begin_time, end_time):
  check_time = datetime.now().time()
  if begin_time < end_time:
    return check_time >= begin_time and check_time <= end_time
  else: # crosses midnight
    return check_time >= begin_time or check_time <= end_time

def get_data():
  with requests.Session() as s:
    initial = s.get(LOGIN_URL)
    soup = BeautifulSoup(initial.content, 'html.parser')

    token = soup.find('input', {'name': '__RequestVerificationToken'}).attrs['value']
    headers = {'__RequestVerificationToken': token}

    s.post(API_LOGIN_URL, data=login_payload, headers=headers)
    page = s.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("span", class_='heading heading--level3 secondary-color margin-bottom')
    if results is None:
      print("Error, credentials are incorrect")
      sys.exit()
    count = int(results.text.split()[0])
    return count

if __name__ == '__main__':
  toaster = ToastNotifier()
  while True:
    if is_time_between(time(OPEN_TIME, 0), time(CLOSE_TIME, 0)):
      print("Polling")
      count = get_data()
      if count < ALERT_THRESHOLD:
        print("Currently "+str(count)+" people in the gym. This is below threshold.")
        toaster.show_toast("Gym is available", "Currently "+str(count)+" people in the gym. This is below threshold.")
      else:
        print("Currently "+str(count)+" people in the gym.")
      time_.sleep(POLLING_RATE)  
