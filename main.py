import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import datetime
import logging
import socket

# Function to load configuration from a file
def load_config(filename='config.txt'):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            config[key] = value
    return config

config = load_config()

# Function to check for temperatures below the specified minimum temperature
def check_temp_below(weather_data, min_temp):
    timeseries = weather_data['properties']['timeseries']
    low_temp_dates = []

    for entry in timeseries:
        time = entry['time']
        temperature = entry['data']['instant']['details']['air_temperature']

        if temperature <= min_temp:
            low_temp_dates.append((time, temperature)) # Appending as a tuple so data can't be changed

    return low_temp_dates

# Your home coordinates in Decimal Degrees - Vågvägen 23, Ludvika
latitude = 60.1496
longitude = 15.1878

# Function to get weather data from yr.no/api
def get_weather_yr(latitude, longitude):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}"
    # Header for user-agent + email
    headers = {
        'User-Agent': f'Plants_Stay_Alive ({config["GMAIL_USERNAME"]})'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to format dates with temperatures below the minimum temperature to make it more readable
def format_dates(low_temp_dates):
    formatted_dates = 'The temperature will drop to 10°C or below on the following date(s):\n\n'
    current_day = None

    for date, temp in low_temp_dates:
        dt = datetime.datetime.fromisoformat(date.replace("Z", "+00:00"))
        day_name = dt.strftime("%A")  # Get the name of the day
        day = dt.strftime("%d")  # Get the day of the month
        month_name = dt.strftime("%B")  # Get the month name
        time_str = dt.strftime("%H:%M")  # Get the time

        formatted_date = f"{day_name} {day} {month_name}"

        if current_day != formatted_date:
            # If it's a new day, print the day name
            if current_day is not None:
                formatted_dates += '\n'  # Adds a blank line between days
            formatted_dates += f'{formatted_date}:\n'
            current_day = formatted_date

        # Add time and temperature
        formatted_dates += f"  {time_str} - {temp}°C\n"

    return formatted_dates

# Main function to check temperature and only send an email once per day by checking the log file
def schedule_weather_yr():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file = 'last_email_sent.txt'

    # Check log file to ensure only one email is sent per day
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            last_sent = f.read().strip()
            if last_sent == today:
                print('Already sent today')
                return

    weather_data = get_weather_yr(latitude, longitude)
    if weather_data:
        low_temp_dates = check_temp_below(weather_data, 10)
        if low_temp_dates:
            formatted_dates = format_dates(low_temp_dates)
            print(formatted_dates)
            send_email('PlantsStayAlive', formatted_dates, config['EMAIL_RECIPIENT'])

            with open(log_file, 'w') as f:
                f.write(today)

        else:
            print('The temperature will not drop to 10°C in the next days.')

# Function to send an email
def send_email(subject, message, to_email):
    from_email = config['GMAIL_USERNAME']
    app_password = config['GMAIL_APP_PASSWORD']

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain')) # 'plain' adds message as plain text

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f'Successfully sent email to {to_email}')
    except smtplib.SMTPException as e:
        print(f'Failed to send email due to SMTP error to {to_email}: {e}')
    except socket.error as e:
        print(f'Failed to send email due to network error to {to_email}: {e}')
    except Exception as e:
        print(f'Failed to send email to {to_email}: {e}')

# Main entry point for the script
if __name__ == '__main__':
    try:
        schedule_weather_yr()
    except Exception as e:
        logging.error('Error occurred: %s', e)
