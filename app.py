from flask import Flask
from dotenv import load_dotenv
import os

from routes.tasks import tasks_bp

load_dotenv()

app = Flask(__name__)
app.register_blueprint(tasks_bp)

@app.route("/")
def home():
    return {"message": "Task Manager API is running!"}

@app.errorhandler(500)
def internal_server_error(_error):
    return {
        "error": "Internal server error"
    }, 500

@app.errorhandler(404)
def not_found(_error):
    return {
        "error": "Resource not found"
    }, 404


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "True")



