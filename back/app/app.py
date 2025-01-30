from flask import Flask, render_template
from config import routes

app = Flask(__name__)

@app.route(routes.INDEX)
def index():
    return render_template('index.html', routes=routes)

@app.route(routes.CHICKEN)
def chicken():
    return render_template('chicken.html', routes=routes, door_status="open")
