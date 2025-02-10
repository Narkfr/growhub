# **Automated Task Scheduling with Cron, Redis, and Celery**

This feature automates task scheduling for different devices, including tasks like opening and closing the chicken coop door based on sunrise and sunset times. It uses a combination of a cron job, Redis, and Celery to manage the task execution flow.

## **How it Works:**

### 1. **Task Generation:**
Each device has a `tasks.py` script, located within the `../devices/device_*` folder. These scripts define tasks to be scheduled using a function called `register_tasks()`.  
When the cron job runs, it gathers all tasks from these device scripts and creates a list of tasks to be scheduled.  

### 2. **Cron Job:**
A cron job is scheduled to run daily at **00:01**. It is responsible for:
- Collecting tasks from all device scripts using the `register_tasks()` function.
- Sending the generated tasks to Redis for future execution.

### 3. **Task Scheduling in Redis:**
Once the cron job collects the tasks, they are added to Redis. Redis acts as a queue where tasks are stored and ready to be executed.  
Each task contains details such as:
- **Topic**: Defines the MQTT topic (e.g., `chicken/door`).
- **Message**: Defines the message to be sent (e.g., "open", "close").
- **Scheduled time**: The time when the task should be executed.

### 4. **Task Execution via Celery:**
Celery is set up to listen for tasks in Redis. It picks up tasks and executes them at the scheduled time.  
The tasks can trigger actions like sending MQTT messages to control the devices (e.g., opening or closing the chicken coop door).

### 5. **Example - Chicken Coop Door:**
For the chicken coop door, the tasks are generated based on the **sunrise** and **sunset** times, which are calculated using the device’s geographical location (latitude and longitude).  
- The door will open **30 minutes after sunrise** and close **30 minutes after sunset**.
- The latitude and longitude are configurable for each device, with Brantôme being the default location.

## **Setup and Configuration:**

### 1. **Device Folder:**
- Each device should have a `tasks.py` file containing a `register_tasks()` function.
- The function should return a list of tasks with the following properties:
  - **topic** (str): The MQTT topic.
  - **message** (str): The MQTT message.
  - **delay** (float): The delay in seconds before the task should be executed.

### 2. **Cron Job:**
- The cron job is configured to run a Python script (e.g., `cron_register_tasks.py`) daily at **00:01**.
- This script will look for all `tasks.py` files in the `../devices/device_*` directories and add the tasks to Redis.

### 3. **Redis:**
Redis should be configured to store tasks. You can inspect the keys in Redis using the `redis-cli` tool.  
The tasks will be stored as serialized data, ready for Celery to process and execute.

### 4. **Celery:**
Celery should be running and connected to Redis. It will pick up the tasks and execute them at the scheduled time, sending the appropriate MQTT messages.
