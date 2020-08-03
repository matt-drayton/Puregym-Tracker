from settings import EMAIL, PIN, POLLING_RATE, ALERT_THRESHOLD
import requests
from bs4 import BeautifulSoup
import time
from win10toast import ToastNotifier

LOGIN_URL = "https://www.puregym.com/login/"
API_LOGIN_URL = "https://www.puregym.com/api/members/login/"
URL = "https://www.puregym.com/members/"


login_payload = {"associateAccount":"false",
                "email":EMAIL,
                "pin":PIN}

def get_data():
  with requests.Session() as s:
    initial = s.get(LOGIN_URL)
    soup = BeautifulSoup(initial.content, 'html.parser')

    token = soup.find('input', {'name': '__RequestVerificationToken'}).attrs['value']
    headers = {'__RequestVerificationToken': token}

    s.post(API_LOGIN_URL, data=login_payload, headers=headers)
    page = s.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("span", class_='heading heading--level3 secondary-color margin-bottom').text

    count = int(results.split()[0])
    return count

if __name__ == '__main__':
  toaster = ToastNotifier()
  while True:
    print("Polling")
    count = get_data()
    if count < ALERT_THRESHOLD:
      print("Currently "+str(count+" people in the gym. This is below threshold."))
      toaster.show_toast("Currently "+count+" people in the gym. This is below threshold.")
    else:
      print("Currently "+str(count)+" people in the gym.")
    time.sleep(POLLING_RATE)  
