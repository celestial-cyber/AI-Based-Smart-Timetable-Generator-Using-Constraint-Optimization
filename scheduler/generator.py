import pymysql
from collections import defaultdict


def generate_timetable():

    conn = pymysql.connect(
        host='localhost',
        port=3307,
        user='root',
        password='',
        database='project_timetable',
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = conn.cursor()

    # Optional: Clear old timetable before generating a new one
    cursor.execute("DELETE FROM timetable")

    # ---------------------------
    # CONFIG
    # ---------------------------
    DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    PERIODS = [1, 2, 3, 4, 5, 6]

    # ---------------------------
    # LOAD DATA
    # ---------------------------
    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    cursor.execute("SELECT * FROM faculty_subjects")
    faculty_subjects = cursor.fetchall()

    cursor.execute("SELECT * FROM rooms")
    rooms = cursor.fetchall()

    cursor.execute("SELECT * FROM classes")
    classes = cursor.fetchall()

    # ---------------------------
    # MAPPINGS
    # ---------------------------
    subject_faculty = defaultdict(list)

    for row in faculty_subjects:
        subject_faculty[row["subject_id"]].append(row["faculty_id"])

    # ---------------------------
    # TRACKING
    # ---------------------------
    class_busy = set()
    faculty_busy = set()
    room_busy = set()

    # ---------------------------
    # CHECK FUNCTION
    # ---------------------------
    def is_free(class_id, faculty_id, room_id, day, period):
        return (
            (class_id, day, period) not in class_busy and
            (faculty_id, day, period) not in faculty_busy and
            (room_id, day, period) not in room_busy
        )

    # ---------------------------
    # GENERATE TIMETABLE
    # ---------------------------
    for cls in classes:

        class_id = cls["class_id"]

        for subject in subjects:

            subject_id = subject["subject_id"]
            hours = subject["hours_per_week"]
            is_lab = subject["is_lab"]

            faculty_list = subject_faculty.get(subject_id, [])

            if not faculty_list:
                print(f"Skipping subject {subject_id}, no faculty assigned")
                continue

            faculty_id = faculty_list[0]

            for i in range(hours):

                assigned = False

                for day in DAYS:
                    for period in PERIODS:
                        for room in rooms:

                            if is_lab and room["room_type"] != "lab":
                                continue

                            if not is_lab and room["room_type"] != "classroom":
                                continue

                            room_id = room["room_id"]

                            if is_free(class_id, faculty_id, room_id, day, period):

                                cursor.execute("""
                                    INSERT INTO timetable
                                    (class_id, subject_id, faculty_id, room_id, day, period)
                                    VALUES (%s,%s,%s,%s,%s,%s)
                                """, (
                                    class_id,
                                    subject_id,
                                    faculty_id,
                                    room_id,
                                    day,
                                    period
                                ))

                                class_busy.add((class_id, day, period))
                                faculty_busy.add((faculty_id, day, period))
                                room_busy.add((room_id, day, period))

                                assigned = True
                                break

                        if assigned:
                            break
                    if assigned:
                        break

                if not assigned:
                    print(f"Could not assign subject {subject_id} for class {class_id}")

    conn.commit()
    cursor.close()
    conn.close()

    print("✅ Timetable generated successfully")


if __name__ == "__main__":
    generate_timetable()