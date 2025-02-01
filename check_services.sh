#!/bin/bash

# Ports and services
FLASK_PORT=5000
MOSQUITTO_SERVICE="mosquitto"
CELERY_SERVICE="celery"
REDIS_PORT=6379

# Checking Flask backend
echo "Checking Flask backend..."
if lsof -i :$FLASK_PORT >/dev/null 2>&1; then
    echo "✅ Flask is running on port $FLASK_PORT"
else
    echo "❌ Flask is not running on port $FLASK_PORT"
fi

echo ""

# Checking Mosquitto service
echo "Checking Mosquitto..."
if pgrep -x "$MOSQUITTO_SERVICE" >/dev/null; then
    echo "✅ Mosquitto is running"
else
    echo "❌ Mosquitto is not running"
fi

echo ""

# Checking Celery worker
echo "Checking Celery worker..."
if pgrep -x "$CELERY_SERVICE" >/dev/null; then
    echo "✅ Celery worker is running"
else
    echo "❌ Celery worker is not running"
fi

echo ""

# Checking Redis service
echo "Checking Redis..."
if lsof -i :$REDIS_PORT >/dev/null 2>&1; then
    echo "✅ Redis is running on port $REDIS_PORT"
else
    echo "❌ Redis is not running on port $REDIS_PORT"
fi
