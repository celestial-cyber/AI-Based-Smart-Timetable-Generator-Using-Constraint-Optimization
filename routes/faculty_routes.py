from flask import render_template, request, redirect
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

    @app.route('/faculty/delete/<int:faculty_id>')
    def delete_faculty(faculty_id):

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM faculty WHERE faculty_id = %s",
            (faculty_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/faculty')

    @app.route('/faculty/edit/<int:faculty_id>', methods=['GET', 'POST'])
    def edit_faculty(faculty_id):

        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':

            faculty_name = request.form['faculty_name']
            email = request.form['email']
            phone = request.form['phone']
            dept_id = request.form['dept_id']
            designation = request.form['designation']
            max_hours = request.form['max_hours']

            update_query = """
            UPDATE faculty
            SET
                faculty_name = %s,
                email = %s,
                phone = %s,
                dept_id = %s,
                designation = %s,
                max_hours = %s
            WHERE faculty_id = %s
            """

            cursor.execute(
                update_query,
                (
                    faculty_name,
                    email,
                    phone,
                    dept_id,
                    designation,
                    max_hours,
                    faculty_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            return redirect('/faculty')

        cursor.execute(
            "SELECT * FROM faculty WHERE faculty_id = %s",
            (faculty_id,)
        )

        faculty_record = cursor.fetchone()

        cursor.close()
        connection.close()

        return render_template(
            'edit_faculty.html',
            faculty=faculty_record
        )