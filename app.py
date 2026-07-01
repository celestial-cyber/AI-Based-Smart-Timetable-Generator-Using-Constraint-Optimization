from flask import Flask
from database.db import get_db_connection
from routes.department_routes import register_department_routes
from routes.faculty_routes import register_faculty_routes
from routes.subject_routes import register_subject_routes
from routes.room_routes import register_room_routes
from routes.class_routes import register_class_routes
from routes.dashboard_routes import register_dashboard_routes
from routes.timetable_routes import register_timetable_routes

app = Flask(__name__)

register_department_routes(app)
register_faculty_routes(app)
register_subject_routes(app)
register_room_routes(app)
register_class_routes(app)
register_dashboard_routes(app)
register_timetable_routes(app)

@app.route('/')
def home():
    return "AI Timetable Generator Running"

if __name__ == "__main__":
    app.run(debug=True)