from flask import render_template, request, redirect
from database.db import get_db_connection


def register_class_routes(app):

    @app.route('/classes', methods=['GET', 'POST'])
    def classes():

        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':

            dept_id = request.form['dept_id']
            year = request.form['year']
            semester = request.form['semester']
            section = request.form['section']
            strength = request.form['strength']

            query = """
            INSERT INTO classes
            (
                dept_id,
                year,
                semester,
                section,
                strength
            )
            VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    dept_id,
                    year,
                    semester,
                    section,
                    strength
                )
            )

            connection.commit()

        cursor.execute("SELECT * FROM classes")
        class_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template(
            'classes.html',
            classes=class_data
        )

    @app.route('/classes/delete/<int:class_id>')
    def delete_class(class_id):

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM classes WHERE class_id = %s",
            (class_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/classes')