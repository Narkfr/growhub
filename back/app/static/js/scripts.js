function scheduleMqttTask(topic, message) {
    fetch('/schedule/mqtt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic, message: message, delay: 20 })
    }).then(response => response.json()).then(data => {
        console.log(data);
        alert("MQTT message scheduled in 2 minutes!");
    });
}

function scheduleMqttTaskAtTime(topic, message) {
    const datetime = new Date(document.getElementById('mqttScheduleTime').value)
        .toISOString()
        .slice(0, 19)
        .replace("T", " "); // "2025-02-09 21:30:00"
    fetch('/schedule/mqtt/datetime', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic, message: message + datetime, datetime: datetime })
    }).then(response => response.json()).then(data => {
        console.log(data);
        alert("MQTT message scheduled at " + datetime);
    });
}

function sendMQTTMessage(topic, message) {
    fetch('/mqtt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, message })
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error));
}