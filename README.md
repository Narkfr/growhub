# GrowHub - Project Technical Documentation

## Overview
This document outlines the technical stack and architecture for the project, which integrates a mobile application, a backend server, connected devices, and communication protocols.

---

## Table of Contents

- [Expo App Initialization](front/README.md)

---

## 1. Frontend
**Technology:** React Native

The frontend is a cross-platform mobile application developed using React Native. It provides the user interface and interacts with the backend API for data retrieval and actions.

### Key Features:
- Cross-platform compatibility (iOS and Android)
- Integration with backend API for user actions and data visualization
- Real-time updates for connected devices

---

## 2. Backend
**Technologies:** Flask, Celery, PostgreSQL

The backend is built using Flask, a lightweight web framework for Python. Celery is used for task scheduling and asynchronous job processing. PostgreSQL serves as the relational database for storing persistent data.

### Components:
1. **Flask:**
   - RESTful API development
   - Authentication and authorization
   - Routing and request handling

2. **Celery:**
   - Background job processing
   - Scheduling tasks (e.g., device commands, data updates)

3. **PostgreSQL:**
   - Persistent data storage
   - Schema for users, devices, and logs

---

## 3. Devices
**Hardware:** Raspberry Pi Pico  
**Software:** MicroPython

The Raspberry Pi Pico devices are programmed using MicroPython. They manage mechanical tasks and interact with the backend server.

### Key Features:
- Lightweight execution of mechanical operations
- Communication with the backend via MQTT
- Support for updates and task execution in real-time

---

## 4. Communication
**Protocols:** Flask API, MQTT

### API (Flask):
- Provides endpoints for:
  - Device registration
  - Command execution
  - Data retrieval

### MQTT:
- Enables lightweight communication between the backend and devices
- Used for real-time messaging and command distribution

---

# Workflow for Scheduled Tasks

## Overview
The system uses a combination of Python, Celery, and Mosquitto to handle scheduled tasks dynamically. Each device module contains a `tasks.py` file that defines the logic for its scheduled tasks.

## Daily Scheduler Execution
- A **CRON job** triggers the script `run_scheduler.py` every day at midnight.
- The script is responsible for discovering all device modules within the `devices` directory and identifying tasks to be scheduled.
- It looks for a `schedule_tasks()` function in each module's `tasks.py` file.

## Task Scheduling with Celery
- Each `schedule_tasks()` function calculates the required times for specific actions (e.g., opening or closing a coop door, activating sprinklers).
- These tasks are then queued using Celery with appropriate execution times (`eta`).

## Communication via Mosquitto
- When a scheduled task executes, it sends a message to the **Mosquitto MQTT server**.
- Messages follow a predefined format and topic structure, which devices subscribe to and act upon in real time.

## Device Listening
- Each device continuously listens to its designated MQTT topic.
- When a message is received, the device performs the corresponding action, such as opening a door, turning on a sprinkler, etc.

## Error Handling
- If `run_scheduler.py` encounters a module without a `schedule_tasks()` function or fails to process a task, it logs the issue and continues parsing other modules.

## Scalability
- Adding a new device only requires creating a new folder under `devices` with a `tasks.py` file that includes the `schedule_tasks()` function.
- The system dynamically discovers and schedules these tasks without further configuration.

---

## Example Workflow

1. **At Midnight (CRON Job)**  
   `run_scheduler.py` runs and identifies all device modules (e.g., `coop`, `sprinkler`).

2. **Task Scheduling**  
   Each module's `schedule_tasks()` function is called to queue tasks with Celery.  
   - Example: Queue a task to open the coop door at sunrise.

3. **Task Execution**  
   At the scheduled time, Celery workers execute the task and send a message to the Mosquitto MQTT server.  
   - Example: A message is sent to the topic `coop/door/open`.

4. **Device Response**  
   The subscribed device listens for the MQTT message and performs the corresponding action.  
   - Example: The coop's door controller opens the door upon receiving the message.

---

This workflow ensures modularity, scalability, and real-time communication between the scheduler and the devices.

---

## Architecture Diagram (Optional)
_Consider adding a diagram to visually represent the interactions between the frontend, backend, and devices._

---

## Future Improvements
- Implement WebSocket communication for real-time updates in the mobile app
- Add device firmware updates via OTA (Over-the-Air)
- Enhance security with encrypted communication channels

---

## Contact
For questions or contributions, please contact the development team.

---

