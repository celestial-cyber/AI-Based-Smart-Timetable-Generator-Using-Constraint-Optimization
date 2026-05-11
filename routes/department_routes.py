from flask import render_template, request
from database.db import get_db_connection


def register_department_routes(app):

    @app.route('/departments', methods=['GET', 'POST'])
    def departments():

        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':

            department_name = request.form['department_name']

            query = """
            INSERT INTO departments (dept_name)
            VALUES (%s)
            """

            cursor.execute(query, (department_name,))
            connection.commit()

        cursor.execute("SELECT * FROM departments")
        department_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template(
            'departments.html',
            departments=department_data
        )