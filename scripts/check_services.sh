#!/bin/bash

# Function to check the status of a service
check_service() {
    service_name=$1
    if systemctl is-active --quiet "$service_name"; then
        echo -e "\033[32m[✔] $service_name is running.\033[0m"
    else
        echo -e "\033[31m[✘] $service_name is NOT running.\033[0m"
    fi
}

# Function to test if a service is accessible via its port
check_service_port() {
    service_name=$1
    port=$2
    if nc -zv 127.0.0.1 $port &>/dev/null; then
        echo -e "\033[32m[✔] $service_name is accessible on port $port.\033[0m"
    else
        echo -e "\033[31m[✘] $service_name is NOT accessible on port $port.\033[0m"
    fi
}

# Checking system services
echo -e "\n\033[1mChecking system services...\033[0m"

# Checking Mosquitto (MQTT)
check_service "mosquitto"

# Checking Redis
check_service "redis-server"

# Checking Celery
check_service "celery"

# Checking external services
echo -e "\n\033[1mChecking external services...\033[0m"

# Checking Flask API (assuming it runs on port 5000)
if curl --silent --head --fail http://127.0.0.1:5000/ > /dev/null; then
    echo -e "\033[32m[✔] Flask API is running on port 5000.\033[0m"
else
    echo -e "\033[31m[✘] Flask API is NOT running on port 5000.\033[0m"
fi

# Checking Mosquitto (using nc to check if port 1883 is open)
check_service_port "Mosquitto" 1883

# Checking Redis (port 6379)
check_service_port "Redis" 6379

# Final rendering
echo -e "\n\033[1mService Check Complete\033[0m"
echo -e ""
