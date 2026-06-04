from flask import render_template, request
from database.db import get_db_connection


def register_subject_routes(app):

    @app.route('/subjects', methods=['GET', 'POST'])
    def subjects():

        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':

            subject_code = request.form['subject_code']
            subject_name = request.form['subject_name']
            hours_per_week = request.form['hours_per_week']
            subject_type = request.form['subject_type']
            semester = request.form['semester']
            dept_id = request.form['dept_id']

            query = """
            INSERT INTO subjects
            (
                subject_code,
                subject_name,
                hours_per_week,
                subject_type,
                semester,
                dept_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    subject_code,
                    subject_name,
                    hours_per_week,
                    subject_type,
                    semester,
                    dept_id
                )
            )

            connection.commit()

        cursor.execute("SELECT * FROM subjects")
        subject_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template(
            'subjects.html',
            subjects=subject_data
        )