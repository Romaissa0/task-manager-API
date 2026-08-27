from flask import Flask
from dotenv import load_dotenv
import os

from routes.tasks import tasks_bp
from routes.auth import auth_bp

from flask_jwt_extended import JWTManager
load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)


app.register_blueprint(tasks_bp)
app.register_blueprint(auth_bp)



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



