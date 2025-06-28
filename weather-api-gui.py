import datetime as dt
import requests
import json
import tkinter as tk
from dotenv import load_dotenv
import os

window = tk.Tk()                           #creating pop up window using Tk()
window.title("Weather App")                #giving title to window 
window.configure(bg="lightblue")

label = tk.Label(window, text='Enter City Name:',font = ("Times New Roman", 16, "bold"), fg="yellow", bg="lightblue")          #creating label button
entry = tk.Entry(window)                                   #creating input field 

label.pack(pady=10)                                            #gives instruction to run this on window 
entry.pack(pady=10)

load_dotenv()
API_KEY = os.getenv("MY_API_KEY")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}"


def get_weather():
    city = entry.get()  #Now we fetch city when user clicks the button
    url = BASE_URL.format(CITY=city, API_KEY=API_KEY)

    response = requests.get(url)

    for widget in window.winfo_children():
      if isinstance(widget, tk.Label) and widget != label and widget != entry:
          widget.destroy()

    if response.status_code == 200:
        data = response.json()

        if 'weather' in data and 'main' in data:
            description = data['weather'][0]['description']
            temp = data['main']['temp']
            temp1 = data['main']['feels_like']
            temp2 = data['main']['temp_max']
            humidity = data['main']['humidity']
            sunrise = data['sys']['sunrise']
            sunset = data['sys']['sunset']

            sunrise_time = dt.datetime.utcfromtimestamp(sunrise).strftime('%Y-%m-%d %H:%M:%S')
            sunset_time = dt.datetime.utcfromtimestamp(sunset).strftime('%Y-%m-%d %H:%M:%S')

            #creating variable to print everything in report 
            weather_report=f"""
        Weather in {city}: {description}\n            
        Temperature: {temp}°C\n
        Feels like: {temp1}°C\n
        Maximum temperature: {temp2}°C\n
        Humidity: {humidity}%\n
        Sunrise time: {sunrise_time}\n
        Sunset time: {sunset_time}\n"""

            result_label = tk.Label(window, text=weather_report, font=("Arial", 10), justify="left", fg="green", bg="lightblue")
            result_label.pack(pady=10)


        else:
            errorlabel = tk.Label(window, text="Error: Weather data not found!", fg="blue")
            errorlabel.pack(pady=10)

    else:
        errorlabel = tk.Label(window, text=f"Request failed, invalid city: {response.status_code}", fg="blue")
        errorlabel.pack()

button = tk.Button(window, text="Get Weather", command=get_weather)      #finally creating button to fetch the weather info and show it bu using get_weather function
button.pack()

window.mainloop() #runs all instructions under tkinter 