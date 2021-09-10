# Puregym Tracker - OUT OF DATE
## Introduction 
This is a tool to monitor activity levels at a chosen home gym. It will alert the user when the number of people in the gym is below a certain threshold. 
## Installation
To install, first clone the repository into a chosen directory.

    git clone "https://github.com/matt-drayton/Puregym-Tracker.git"
Remember that you may have to provide github credentials depending on whether I make this public or not.

Then, navigate to the directory and enter the following command:

    pip install -r requirements.txt
    
Currently this only seems to work on PIP versions 19.x.x. This seems to be related to the custom version of `win10toast` that is used for the behaviour when clicking notifications.

Enter your Puregym credentials and chosen settings into `settings.py`

Finally, run the program by entering `python puregym-tracker.py`.

Note: You can also run the program using `pythonw puregym-tracker.py` which will run the program in the background. This means you will still get notifications but will not be able to see the program polling. 

## Usage
Simply run the script using either `python puregym-tracker.py` or `pythonw puregym-tracker.py`. When the gym has fewer people than the chosen threshold, a Windows 10 notification will appear informing the user of this. Clicking the notification will mute the program for 1hr.
## Settings
The `settings.py` file is used to configure the program. Below is an explanation of each field:

 - EMAIL - The email address associated with your Puregym account
 - PIN - The PIN associated with your Puregym account
 - POLLING_RATE - How often, in seconds, to make the request to Puregym. Note: I have not experimented with how Puregym reacts to many requests in a short period of time.
 - ALERT_THRESHOLD - Maximum number of people in the gym, below which the user will be alerted.
 - OPEN_TIME - The opening hour of the gym (in the format 0-23)
 - CLOSE_TIME - The closing our of the gym (in the format 0-23)
