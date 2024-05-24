import requests
from datetime import datetime, timedelta


resp = requests.get('http://challenge.nahamcon.com:31609/status').text

impt = resp.split('...\n')[1]

# Uptime in days, hours, and minutes
uptime_days = int(impt.split(' days')[0])
uptime_hours = int(impt.split(' hours')[0][-2:])
uptime_minutes = int(impt.split(' minutes')[0][-2:])
print("DAYS: ", uptime_days,"\nHOURS:", uptime_hours,"\nMINS: ", uptime_minutes)

# Current time
current_time = datetime.now()

# Calculate total uptime in seconds
total_uptime_seconds = (uptime_days * 24 * 3600) + (uptime_hours * 3600) + (uptime_minutes * 60)

# Calculate the start time
start_time = current_time - timedelta(seconds=total_uptime_seconds)

# Format the start time
start_time_formatted = start_time.strftime("%Y%m%d%H%M")

# Print the start time
print("\napp.secret_key:\nTHE_REYNOLDS_PAMPHLET-"+start_time_formatted)