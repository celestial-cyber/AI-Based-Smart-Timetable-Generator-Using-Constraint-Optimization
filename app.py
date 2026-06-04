from flask import Flask, jsonify
from database.db import get_db_connection
from routes.department_routes import register_department_routes
from routes.faculty_routes import register_faculty_routes
from routes.subject_routes import register_subject_routes
app = Flask(__name__)

register_department_routes(app)
register_faculty_routes(app)
register_subject_routes(app)


@app.route('/')
def home():
    return "AI Timetable Generator Running"





if __name__ == "__main__":
    app.run(debug=True)