# The following script will be used for the countdown in home.html

# Import libraries
import datetime
from django.shortcuts import render

# Define the function that calculates the remaining time
def countdown(request):
    date = "2024-12-06 00:00:00"
    today = datetime.datetime.now
    countdown_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    difference = countdown_date - now
    difference = difference.total_seconds()
    return render(request, 'home.html', {'total_time': difference})




