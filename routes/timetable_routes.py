from flask import render_template, redirect, make_response
from database.db import get_db_connection
from scheduler.generator import generate_timetable

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def register_timetable_routes(app):

    # ----------------------------------------
    # View Timetable
    # ----------------------------------------
    @app.route('/timetable')
    def timetable():

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            t.timetable_id,
            d.dept_name,
            c.year,
            c.semester,
            c.section,
            s.subject_code,
            s.subject_name,
            f.faculty_name,
            r.room_name,
            t.day,
            t.period

        FROM timetable t

        JOIN classes c
            ON t.class_id = c.class_id

        JOIN departments d
            ON c.dept_id = d.dept_id

        JOIN subjects s
            ON t.subject_id = s.subject_id

        JOIN faculty f
            ON t.faculty_id = f.faculty_id

        JOIN rooms r
            ON t.room_id = r.room_id

        ORDER BY
            c.class_id,
            FIELD(t.day,'Mon','Tue','Wed','Thu','Fri'),
            t.period
        """

        cursor.execute(query)
        timetable_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return render_template(
            "timetable.html",
            timetable=timetable_data
        )

    # ----------------------------------------
    # Generate Timetable
    # ----------------------------------------
    @app.route('/generate-timetable')
    def generate():

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM timetable")
        connection.commit()

        cursor.close()
        connection.close()

        generate_timetable()

        return redirect('/timetable')

    # ----------------------------------------
    # Delete Timetable
    # ----------------------------------------
    @app.route('/delete-timetable')
    def delete_timetable():

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM timetable")
        connection.commit()

        cursor.close()
        connection.close()

        return redirect('/timetable')

    # ----------------------------------------
    # Export PDF
    # ----------------------------------------
    @app.route('/export-pdf')
    def export_pdf():

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        SELECT
            d.dept_name,
            c.year,
            c.semester,
            c.section,
            t.day,
            t.period,
            s.subject_code,
            s.subject_name,
            f.faculty_name,
            r.room_name

        FROM timetable t

        JOIN classes c
            ON t.class_id = c.class_id

        JOIN departments d
            ON c.dept_id = d.dept_id

        JOIN subjects s
            ON t.subject_id = s.subject_id

        JOIN faculty f
            ON t.faculty_id = f.faculty_id

        JOIN rooms r
            ON t.room_id = r.room_id

        ORDER BY
            c.class_id,
            FIELD(t.day,'Mon','Tue','Wed','Thu','Fri'),
            t.period
        """

        cursor.execute(query)
        timetable = cursor.fetchall()

        cursor.close()
        connection.close()

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()
        elements = []

        elements.append(
            Paragraph("<b>AI Timetable Report</b>", styles["Title"])
        )

        data = [[
            "Department",
            "Year",
            "Semester",
            "Section",
            "Day",
            "Period",
            "Subject Code",
            "Subject",
            "Faculty",
            "Room"
        ]]

        for row in timetable:

            data.append([
                row["dept_name"],
                row["year"],
                row["semester"],
                row["section"],
                row["day"],
                row["period"],
                row["subject_code"],
                row["subject_name"],
                row["faculty_name"],
                row["room_name"]
            ])

        table = Table(data)

        table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 10)

        ]))

        elements.append(table)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        response = make_response(pdf)

        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = (
            "attachment; filename=Timetable_Report.pdf"
        )

        return response