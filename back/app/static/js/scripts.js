function scheduleMqttTaskAtDelay(event) {
    event.preventDefault(); // Prevent page reload

    // Get form data
    const formData = new FormData(event.target);
    const topic = formData.get("topic");
    const message = formData.get("message");
    const delay = parseInt(formData.get("delay"), 10); // Convert to integer
    fetch('/schedule/mqtt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic, message: message, delay: delay })
    }).then(response => response.json()).then(data => {
        console.log(data);
        alert(`MQTT message scheduled in ${delay} seconds!`);
    });
}

function scheduleMqttTaskAtTime(event) {
    event.preventDefault();
    console.log(event);
    // Get form data
    const formData = new FormData(event.target);
    const topic = formData.get("topic");
    const message = formData.get("message");
    const datetime = new Date(formData.get("datetime"))
        .toISOString()
        .slice(0, 19)
        .replace("T", " "); // Format: "YYYY-MM-DD HH:MM:SS"
    fetch('/schedule/mqtt/datetime', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic, message: message + datetime, datetime: datetime })
    }).then(response => response.json()).then(data => {
        console.log(data);
        alert(`MQTT message scheduled at ${datetime}`);
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