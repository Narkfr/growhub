# GrowHub - Project Technical Documentation

## Overview
This document outlines the technical stack and architecture for the project, which integrates a mobile application, a backend server, connected devices, and communication protocols.

---

## Table of Contents

- [Expo App Initialization](front/README.md)
- [Workflow for scheduled tasks](docs/workflow_scheduled_tasks.md)

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

