import requests
from datetime import datetime
import smtplib
import time

# Variables to stored login Parameters and Location
my_email = "Email Goes Here"
password = "Password Goes Here"
MY_LAT = 7.419325 # Your latitude
MY_LONG = 3.970969 # Your longitude

# Function to check if the start issover head
def iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

# Function to check if it is night
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset and  time_now <= sunrise:
        return True


# BONUS: run the code every 60 seconds.
while True:
    time.sleep(60)
    if iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="ik.umez@yahoo.com",
                msg=f"Subject:Iss is Over Your Head\n\n Please fill free to run outside and check for the fast moving star")







