# Workflow for Scheduled jobs

## Overview
The system uses a combination of Python, Celery, and Mosquitto to handle scheduled jobs dynamically. Each device module contains a `jobs.py` file that defines the logic for its scheduled jobs.

## Daily Scheduler Execution
- A **CRON job** triggers the script `run_scheduler.py` every day at midnight.
- The script is responsible for discovering all device modules within the `devices` directory and identifying jobs to be scheduled.
- It looks for a `schedule_jobs()` function in each module's `jobs.py` file.

## job Scheduling with Celery
- Each `schedule_jobs()` function calculates the required times for specific actions (e.g., opening or closing a coop door, activating sprinklers).
- These jobs are then queued using Celery with appropriate execution times (`eta`).

## Communication via Mosquitto
- When a scheduled job executes, it sends a message to the **Mosquitto MQTT server**.
- Messages follow a predefined format and topic structure, which devices subscribe to and act upon in real time.

## Device Listening
- Each device continuously listens to its designated MQTT topic.
- When a message is received, the device performs the corresponding action, such as opening a door, turning on a sprinkler, etc.

## Error Handling
- If `run_scheduler.py` encounters a module without a `schedule_jobs()` function or fails to process a job, it logs the issue and continues parsing other modules.

## Scalability
- Adding a new device only requires creating a new folder under `devices` with a `jobs.py` file that includes the `schedule_jobs()` function.
- The system dynamically discovers and schedules these jobs without further configuration.

---

## Example Workflow

1. **At Midnight (CRON Job)**  
   `run_scheduler.py` runs and identifies all device modules (e.g., `coop`, `sprinkler`).

2. **job Scheduling**  
   Each module's `schedule_jobs()` function is called to queue jobs with Celery.  
   - Example: Queue a job to open the coop door at sunrise.

3. **job Execution**  
   At the scheduled time, Celery workers execute the job and send a message to the Mosquitto MQTT server.  
   - Example: A message is sent to the topic `coop/door/open`.

4. **Device Response**  
   The subscribed device listens for the MQTT message and performs the corresponding action.  
   - Example: The coop's door controller opens the door upon receiving the message.

---

This workflow ensures modularity, scalability, and real-time communication between the scheduler and the devices.

---