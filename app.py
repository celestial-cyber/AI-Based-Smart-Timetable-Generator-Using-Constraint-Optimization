from flask import Flask, jsonify
from database.db import get_db_connection

app = Flask(__name__)


@app.route('/')
def home():
    return "AI Timetable Generator Running"


@app.route('/faculty')
def faculty():

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM faculty"
    cursor.execute(query)

    faculty_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(faculty_data)


if __name__ == "__main__":
    app.run(debug=True)