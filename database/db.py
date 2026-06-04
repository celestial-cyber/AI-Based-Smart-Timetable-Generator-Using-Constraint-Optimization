import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='',
        database='project_timetable',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection