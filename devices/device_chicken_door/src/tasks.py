from astral.sun import sun
from astral import LocationInfo
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
import pytz
import json

# Default location: Brantôme, France
DEFAULT_LAT = 45.3667
DEFAULT_LON = 0.6492

def register_tasks():
    """Generates tasks for opening and closing the chicken coop door based on sunrise and sunset times,
    using the correct timezone for the given coordinates."""

    # Get the current date
    today = (datetime.now() + timedelta(days=1)).date()
    
    # Get the timezone based on latitude and longitude
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lng=0.6492, lat=45.3667)
    if tz_name is None:
        raise ValueError("Could not determine timezone for given coordinates.")
    
    # Get the timezone object
    timezone = pytz.timezone(tz_name)

    # Define the location for Astral
    location = LocationInfo(latitude=DEFAULT_LAT, longitude=DEFAULT_LON)
    
    # Compute sunrise and sunset times in local time
    s = sun(location.observer, date=today)
    sunset = s["sunset"].astimezone(timezone) + timedelta(minutes=30)
    sunrise = s["sunrise"].astimezone(timezone) + timedelta(minutes=30)
 
    # Get the current time in the same timezone
    now = datetime.now(timezone)

    # Calculate the delay in seconds before task execution
    open_delay = max(0, (sunrise - now).total_seconds())
    close_delay = max(0, (sunset - now).total_seconds())

    # Create the task list
    tasks = [
        {"topic": "chicken/door", "message": "open", "delay": open_delay},
        {"topic": "chicken/door", "message": "close", "delay": close_delay}
    ]

    return tasks

# Execute the script
if __name__ == "__main__":
    tasks = register_tasks()
    print(json.dumps(tasks, indent=2))
