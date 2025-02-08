# The following script will be used for the countdown in home.html

# Import libraries
import datetime

# Define the function that calculates the remaining time
date = "2025-04-10 09:00:00"
today = datetime.datetime.now()
countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

difference = countdown_date - today
difference = difference.total_seconds()

print(difference)



