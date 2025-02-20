function scheduleMqttTask(event) {
    event.preventDefault(); // Prevent page reload

    // Retrieve form data
    const formData = new FormData(event.target);
    const topic = formData.get("topic");
    const message = formData.get("message");
    const delay = formData.get("delay") ? parseInt(formData.get("delay"), 10) : null;
    const datetimeRaw = formData.get("datetime");
    const datetime = datetimeRaw
        ? new Date(datetimeRaw).toISOString().slice(0, 19).replace("T", " ")
        : null;

    // Build request payload
    const requestBody = {
        topic,
        message,
        ...(delay && { delay }),
        ...(datetime && { datetime })
    };

    // Send request to the backend
    fetch('/mqtt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const alertMessage = datetime
            ? `MQTT message scheduled at ${datetime}!`
            : `MQTT message scheduled in ${delay} seconds!`;
        alert(alertMessage);
    })
    .catch(error => console.error('Error:', error));
}
