from flask import render_template
from database.db import get_db_connection


def register_dashboard_routes(app):

    @app.route('/dashboard')
    def dashboard():

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM departments")
        departments = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM faculty")
        faculty = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM subjects")
        subjects = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM rooms")
        rooms = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM classes")
        classes = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return render_template(
            'dashboard.html',
            departments=departments,
            faculty=faculty,
            subjects=subjects,
            rooms=rooms,
            classes=classes
        )