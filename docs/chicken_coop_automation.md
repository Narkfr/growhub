
# Chicken Coop Door Automation

## Overview

The Chicken Coop Door Automation system is designed to control the opening and closing of the chicken coop door based on the sunrise and sunset times. It uses Celery for task scheduling and Redis to store tasks for execution. The system allows you to set a configurable delay after sunrise and sunset for the door opening and closing actions.

## Features

- **Automatic Door Opening**: The door opens 30 minutes after sunrise.
- **Automatic Door Closing**: The door closes 30 minutes after sunset.
- **Configurability**: Latitude and longitude can be adjusted to suit different locations. By default, the system uses the coordinates for Brantôme.
- **Task Scheduling**: Tasks are scheduled and executed automatically by Celery, using Redis to store task details.

## Configuration

### Latitude and Longitude

The system uses the `sunrise-sunset` API to calculate the times of sunrise and sunset based on the provided latitude and longitude. By default, the coordinates for Brantôme are used, but you can configure them as needed.

To change the latitude and longitude, modify the following values:

```python
latitude = 45.4635
longitude = 0.6348
```

Replace `45.4635` and `0.6348` with the coordinates for your location.

### Task Scheduling

The task of opening and closing the door is scheduled based on the time of sunrise and sunset. The system calculates the following:

- **Opening**: Sunrise time + 30 minutes.
- **Closing**: Sunset time + 30 minutes.

These tasks are sent to the Redis queue and then executed by Celery, which processes them at the scheduled times.

## Example Task Schedule

After the cron job executes, the following tasks are created:

```json
[
  {
    "topic": "chicken/door",
    "message": "open",
    "delay": "30 minutes after sunrise"
  },
  {
    "topic": "chicken/door",
    "message": "close",
    "delay": "30 minutes after sunset"
  }
]
```

These tasks are then sent to Redis for execution.

## Running the System

1. **Set Up Cron Job**: A cron job is configured to run at 00:01 AM every day to generate and schedule the tasks for the next day.
2. **Celery Worker**: Ensure that the Celery worker is running to process the tasks from Redis.

To start the Celery worker, use the following command:

```bash
celery -A app.celery worker --loglevel=info
```

3. **Monitor Tasks**: You can monitor the task queue and ensure the tasks are being executed correctly.

## Future Improvements

- **Manual Override**: Ability to manually control the door via an API or a button.
- **Error Handling**: Improve error handling for edge cases such as incorrect sunrise/sunset data.

## Conclusion

This system automates the daily opening and closing of the chicken coop door based on the natural light cycle, saving time and ensuring your chickens are safely housed according to the time of day. The system is fully configurable and can be extended for more devices or customized for specific use cases.
