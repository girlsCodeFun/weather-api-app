import requests
import pandas as pd
from unidecode import unidecode
from translate import Translator
from datetime import datetime

# 1. Prepare variables
api_key = "7d164510ae104c8fa46212207230112"

# 2. Connect to API
while True:
    city = input("Enter the city to get weather data from: ")
    city_unidecoded = unidecode(city)
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city_unidecoded}&aqi=yes"
    try:
        response = requests.get(url)  # get = select
        if response.status_code == 200:
            response = response.json()
            break
        else:
            if response.status_code == 400:
                print("Error! Invalid city input. Try again.")
    except:
        print("Unable to connect to API.")
        exit()

menu_message = f"Select what you want to display for {city}: " \
               "\n1) Temperature" \
               "\n2) Pressure" \
               "\n3) Humidity" \
               "\n4) All above" \
               "\nYour choice: "

while True:
    try:
        # Jeżeli użytkownik poda wartość którą uda się skonwertować do integera, to przechodzimy do linijki 21
        user_choice = int(input(menu_message))
        # jeżeli użytkownik wpisze liczbe z zakresu 1-4
        if 0 < user_choice < 5:
            break  # wychodzimy z pętli nieskończoności
        else:
            print(f"\n{user_choice} is not a supported option. Try again.")
    except ValueError:
        print("\nInvalid input. Try again.")

# 3. Prepare variables with weather information
temp_c = response['current']['temp_c']
pressure = response['current']['pressure_mb']
humidity = response['current']['humidity']

# 4. Display general weather overview message
translator = Translator(to_lang='pl')
weather_text = response['current']['condition']['text']
weather_text_pl = translator.translate(weather_text)

print(f"Weather overview: {weather_text} (PL: {weather_text_pl}).")


# 5. Prepare function to display emojis
def display_weather_icon(temp):
    if temp > 15:
        print("☀️")
    elif temp <= 0:
        print("❄️")
    elif 15 > temp > 0:
        print("🌤️")


# 6. Display weather data based on the user input
if user_choice == 1:
    display_weather_icon(temp=temp_c)
    print(f"Temperature for {city} is: {temp_c}°C degrees.")
elif user_choice == 2:
    print(f"Pressure for {city} is: {pressure} mb.")
elif user_choice == 3:
    print(f"Humidity for {city} is: {humidity}%.")
elif user_choice == 4:
    display_weather_icon(temp=temp_c)
    print(f"Temperature for {city} is: {temp_c}°C degrees.")
    print(f"Pressure for {city} is: {pressure} mb.")
    print(f"Humidity for {city} is: {humidity}%.")
else:
    print("Invalid data.")


# 7. Save weather data to file

# Prepare date
current_date = datetime.now()

# Prepare data for pandas dataframe
data = {'Miasto': city,
        'Temperatura (°C)': temp_c,
        'Ciśnienie': pressure,
        'Wilgotność': humidity,
        'Stan pogodowy': weather_text_pl,
        'Data': current_date.strftime("%Y-%m-%d %H:%M")
        }

# Create pandas dataframe
df = pd.DataFrame([data])

# Save data to excel file
excel_filename = f'dane_pogoda_{city.lower()}_{current_date.strftime("%Y%m%d")}.xlsx'  # lower() - changes city name to lowercase
df.to_excel(excel_filename, index=False, engine='openpyxl')
