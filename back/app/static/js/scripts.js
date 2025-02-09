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
    const datetimeInput = document.getElementById('mqttScheduleTime').value;
    fetch('/schedule/mqtt/datetime', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic, message: message, datetime: datetimeInput })
    }).then(response => response.json()).then(data => {
        console.log(data);
        alert("MQTT message scheduled at " + datetimeInput);
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