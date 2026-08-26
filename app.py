from flask import Flask
from routes.tasks import tasks_bp


app = Flask(__name__)

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

app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True)



