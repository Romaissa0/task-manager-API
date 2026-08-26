from flask import Flask
from routes.tasks import tasks_bp


app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Task Manager API is running!"}




app.register_blueprint(tasks_bp)

if __name__ == "__main__":
    app.run(debug=True)



