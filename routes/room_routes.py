from flask import render_template, request, redirect
from database.db import get_db_connection


def register_room_routes(app):

    @app.route('/rooms', methods=['GET', 'POST'])
    def rooms():

        connection = get_db_connection()
        cursor = connection.cursor()

        if request.method == 'POST':

            room_name = request.form['room_name']
            room_type = request.form['room_type']
            capacity = request.form['capacity']

            query = """
            INSERT INTO rooms
            (
                room_name,
                room_type,
                capacity
            )
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                query,
                (
                    room_name,
                    room_type,
                    capacity
                )
            )

            connection.commit()

        cursor.execute("SELECT * FROM rooms")
        room_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template(
            'rooms.html',
            rooms=room_data
        )

    @app.route('/rooms/delete/<int:room_id>')
    def delete_room(room_id):

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM rooms WHERE room_id = %s",
            (room_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/rooms')