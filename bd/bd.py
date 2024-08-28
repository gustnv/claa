from flask import session
import mysql.connector
import bcrypt
from datetime import datetime

config = {
    'user': 'root',
    'password': 'P4ssw0rd!',
    'host': '127.0.0.1',
    'database': 'claa',
    'raise_on_warnings': True
}


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def login(email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = "select password from tutors where email = %s"
    cursor.execute(query, (email, ))

    result = cursor.fetchone()
    cursor.close()
    cnx.close()

    if result is None:
        return False

    stored_password = result[0]
    if bcrypt.checkpw(password.encode('utf-8'),
                      stored_password.encode('utf-8')):
        return True
    else:
        return False


def tutor_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from tutors where email = %s")
    cursor.execute(query, (email, ))
    tutor_exists = cursor.fetchone()

    cursor.close()
    cnx.close()

    if tutor_exists is None:
        return False
    else:
        return True


def insert_tutor(name, status_claa, email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "insert into tutors (name, status_claa, email, password) values (%s,"
        " %s, %s, %s)")

    hashed_password = hash_password(password)

    data = (name, status_claa, email, hashed_password)
    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


def group_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from claa.groups where email = %s")
    cursor.execute(query, (email, ))
    group_exists = cursor.fetchone()

    cursor.close()
    cnx.close()

    if group_exists is None:
        return False
    else:
        return True


def insert_group(name, email, insta, page, nof_scholarships, nof_volunteers,
                 address, campus, center):
    # todo fix
    email_tutor = "1@1"  # it should exists in tutors table

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "insert into claa.groups "
        "(name, email, instagram, webpage, nof_scholarships, nof_volunteers,"
        " address, campus, center, email_tutor) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    data = (name, email, insta, page, nof_scholarships,
            nof_volunteers, address, campus, center, email_tutor)

    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


def reset_report_session():
    # session_keys = [
    #     'scheduled_activities', 'unscheduled_activities',
    #     'activities_articulation', 'politics_articulation',
    #     'selection_students', 'permanence_students',
    #     'ufsc_target_public', 'society_target_public',
    #     'infrastructure_condition', 'infrastructure_description',
    #     'tools_condition', 'tools_description',
    #     'costing_condition', 'costing_description']
    #
    # for key in session_keys:
    #     session.pop(key, None)
    session.clear()


def insert_report():
    for key, value in session.items():
        print(f"{key}: {value}")

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "INSERT INTO reports (activities_articulation, politics_articulation, "
        "selection_students, permanence_students, ufsc_target_public, "
        "society_target_public, infrastructure_condition, "
        "infrastructure_description, tools_condition, tools_description, "
        "costing_condition, costing_description, year, group_email) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    group_email = "1@1"  # Replace with dynamic value as needed

    data = (
        session.get('activities_articulation'),
        session.get('politics_articulation'),
        session.get('selection_students'),
        session.get('permanence_students'),
        session.get('ufsc_target_public'),
        session.get('society_target_public'),
        session.get('infrastructure_condition'),
        session.get('infrastructure_description'),
        session.get('tools_condition'),
        session.get('tools_description'),
        session.get('costing_condition'),
        session.get('costing_description'),
        datetime.now().year,
        group_email
    )

    cursor.execute(query, data)
    report_id = cursor.lastrowid

    # Insert into scheduled_activities table
    for activity in session.get('scheduled_activities', []):
        query = (
            "INSERT INTO scheduled_activities (name, carrying_out,"
            " total_hours, teaching_hours, research_hours, extension_hours,"
            " report_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )

        data = (
            activity['name'],
            activity['carrying_out'],
            activity['total_hours'],
            activity['teaching_hours'],
            activity['research_hours'],
            activity['extension_hours'],
            report_id
        )

        cursor.execute(query, data)

    # Insert into unscheduled_activities table
    for activity in session.get('unscheduled_activities', []):
        query = (
            "INSERT INTO unscheduled_activities (name, justification,"
            " total_hours, teaching_hours, research_hours, extension_hours,"
            " report_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )

        data = (
            activity['name'],
            activity['justification'],
            activity['total_hours'],
            activity['teaching_hours'],
            activity['research_hours'],
            activity['extension_hours'],
            report_id
        )

        cursor.execute(query, data)

    cnx.commit()
    cursor.close()
    cnx.close()

    reset_report_session()
