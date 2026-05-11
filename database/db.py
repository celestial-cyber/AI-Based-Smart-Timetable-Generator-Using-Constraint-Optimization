import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='project_timetable',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection