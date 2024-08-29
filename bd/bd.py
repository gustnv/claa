from flask import session
import mysql.connector
from mysql.connector import Error
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
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT name, email, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    if result is None:
        return False

    stored_password = result['password']
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        user = {
            'name': result['name'],
            'email': result['email']
        }
        return user
    else:
        return False


def get_name_user_by_email(email):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT name FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result[0] if result else None


def claa_member(email):
    if not tutor_exists(email):
        return False

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT status_claa FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        status_claa = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    if status_claa and status_claa[0] in ('holder', 'substitute'):
        return True
    else:
        return False


def tutor_exists(email):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT 1 FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        tutor_exists = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return tutor_exists is not None


def insert_tutor(name, status_claa, email, password):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = (
            "INSERT INTO users (name, status_claa, email, password) VALUES (%s, %s, %s, %s)"
        )

        hashed_password = hash_password(password)
        data = (name, status_claa, email, hashed_password)
        cursor.execute(query, data)
        cnx.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def report_exists(email):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT 1 FROM reports WHERE email_group = %s AND year = %s"
        cursor.execute(query, (email, datetime.now().year))
        report_exists = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return report_exists is not None


def tutor_has_group(email):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT 1 FROM groups WHERE email_tutor = %s"
        cursor.execute(query, (email,))
        tutor_has_group = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return tutor_has_group is not None


def get_group_by_email_tutor(email_tutor):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT * FROM claa.groups WHERE email_tutor = %s"
        cursor.execute(query, (email_tutor,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result


def group_exists(email):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT 1 FROM claa.groups WHERE email = %s"
        cursor.execute(query, (email,))
        group_exists = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return group_exists is not None


def update_group(form_data, email_tutor):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = """
        UPDATE claa.groups 
        SET name = %s, instagram = %s, webpage = %s, nof_scholarships = %s,
            nof_volunteers = %s, address = %s, campus = %s, center = %s
        WHERE email_tutor = %s
        """

        cursor.execute(query, (
            form_data['name'],
            form_data['insta'],
            form_data['page'],
            form_data['nof_scholarships'],
            form_data['nof_volunteers'],
            form_data['address'],
            form_data['campus'],
            form_data['center'],
            email_tutor
        ))
        cnx.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def insert_group(form_data, email_tutor):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = (
            "INSERT INTO claa.groups "
            "(name, email, instagram, webpage, nof_scholarships, nof_volunteers, "
            "address, campus, center, email_tutor) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        data = (
            form_data['name'], form_data['email'], form_data['insta'],
            form_data['page'], form_data['nof_scholarships'], form_data['nof_volunteers'],
            form_data['address'], form_data['campus'], form_data['center'], email_tutor
        )

        cursor.execute(query, data)
        cnx.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def get_email_group_by_tutor(email_tutor):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT email FROM claa.groups WHERE email_tutor = %s"
        cursor.execute(query, (email_tutor,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result[0] if result else None


def get_report_by_email_group(email_group):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT * FROM claa.reports WHERE email_group = %s"
        cursor.execute(query, (email_group,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result


def get_session(key):
    pass


def reset_session():
    email_user = session['email_user']
    session.clear()
    session['email_user'] = email_user


def insert_report(email_group):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = (
            "INSERT INTO reports (activities_articulation, politics_articulation, "
            "selection_students, permanence_students, ufsc_target_public, "
            "society_target_public, infrastructure_condition, "
            "infrastructure_description, tools_condition, tools_description, "
            "costing_condition, costing_description, year, email_group) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

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
            email_group
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

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def update_report(email_group):
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # SQL query to update the report data
        query = """
        UPDATE reports 
        SET activities_articulation = %s, 
            politics_articulation = %s, 
            selection_students = %s, 
            permanence_students = %s, 
            ufsc_target_public = %s, 
            society_target_public = %s, 
            infrastructure_condition = %s, 
            infrastructure_description = %s, 
            tools_condition = %s, 
            tools_description = %s, 
            costing_condition = %s, 
            costing_description = %s
        WHERE email_group = %s AND year = %s
        """

        # Prepare the data tuple using session data
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
            email_group,
            datetime.now().year
        )

        cursor.execute(query, data)
        cnx.commit()

        # Update scheduled activities
        report_id_query = "SELECT id FROM reports WHERE email_group = %s AND year = %s"
        cursor.execute(report_id_query, (email_group, datetime.now().year))
        report_id = cursor.fetchone()[0]

        # Delete existing scheduled activities
        delete_scheduled_activities = "DELETE FROM scheduled_activities WHERE report_id = %s"
        cursor.execute(delete_scheduled_activities, (report_id,))

        # Insert new scheduled activities
        for activity in session.get('scheduled_activities', []):
            insert_scheduled = (
                "INSERT INTO scheduled_activities (name, carrying_out,"
                " total_hours, teaching_hours, research_hours, extension_hours,"
                " report_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )

            data_scheduled = (
                activity['name'],
                activity['carrying_out'],
                activity['total_hours'],
                activity['teaching_hours'],
                activity['research_hours'],
                activity['extension_hours'],
                report_id
            )

            cursor.execute(insert_scheduled, data_scheduled)

        # Delete existing unscheduled activities
        delete_unscheduled_activities = "DELETE FROM unscheduled_activities WHERE report_id = %s"
        cursor.execute(delete_unscheduled_activities, (report_id,))

        # Insert new unscheduled activities
        for activity in session.get('unscheduled_activities', []):
            insert_unscheduled = (
                "INSERT INTO unscheduled_activities (name, justification,"
                " total_hours, teaching_hours, research_hours, extension_hours,"
                " report_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            )

            data_unscheduled = (
                activity['name'],
                activity['justification'],
                activity['total_hours'],
                activity['teaching_hours'],
                activity['research_hours'],
                activity['extension_hours'],
                report_id
            )

            cursor.execute(insert_unscheduled, data_unscheduled)

        cnx.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
