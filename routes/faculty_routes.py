from flask import render_template, request
from database.db import get_db_connection


def register_faculty_routes(app):

    @app.route('/faculty', methods=['GET', 'POST'])
    def faculty():

        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':

            faculty_name = request.form['faculty_name']
            email = request.form['email']
            phone = request.form['phone']
            dept_id = request.form['dept_id']
            designation = request.form['designation']
            max_hours = request.form['max_hours']

            query = """
            INSERT INTO faculty
            (
                faculty_name,
                email,
                phone,
                dept_id,
                designation,
                max_hours
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    faculty_name,
                    email,
                    phone,
                    dept_id,
                    designation,
                    max_hours
                )
            )

            connection.commit()

        cursor.execute("SELECT * FROM faculty")
        faculty_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template(
            'faculty.html',
            faculty=faculty_data
        )