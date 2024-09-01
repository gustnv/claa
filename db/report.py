from flask import session
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from db.config import config


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


def get_scheduled_activities(report_id):
    try:
        # Establish database connection
        # Make sure `config` is defined with your database credentials
        cnx = mysql.connector.connect(**config)
        # Use dictionary cursor to get results as dictionaries
        cursor = cnx.cursor(dictionary=True)

        # Define the query
        query = """
        SELECT id, name, carrying_out, total_hours, 
               teaching_hours, research_hours, extension_hours 
        FROM scheduled_activities 
        WHERE report_id = %s
        """

        # Execute the query
        cursor.execute(query, (report_id,))
        result = cursor.fetchall()  # Fetch all results

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        # Clean up database resources
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result


def get_unscheduled_activities(report_id):
    try:
        # Establish database connection
        # Make sure `config` is defined with your database credentials
        cnx = mysql.connector.connect(**config)
        # Use dictionary cursor to get results as dictionaries
        cursor = cnx.cursor(dictionary=True)

        # Define the query
        query = """
        SELECT id, name, justification, total_hours, 
               teaching_hours, research_hours, extension_hours 
        FROM unscheduled_activities 
        WHERE report_id = %s
        """

        # Execute the query
        cursor.execute(query, (report_id,))
        result = cursor.fetchall()  # Fetch all results

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        # Clean up database resources
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result


def reset_report_session():
    # Reset the specified session keys to None
    session['activities_articulation'] = ""
    session['politics_articulation'] = ""
    session['selection_students'] = ""
    session['permanence_students'] = ""
    session['ufsc_target_public'] = ""
    session['society_target_public'] = ""
    session['infrastructure_condition'] = ""
    session['infrastructure_description'] = ""
    session['tools_condition'] = ""
    session['tools_description'] = ""
    session['costing_condition'] = ""
    session['costing_description'] = ""
    session['scheduled_activities'] = []
    session['unscheduled_activities'] = []


def transfer_report(from_email, to_email):
    """Transfers all reports from one group to another in the database."""
    try:
        # Establishing connection to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Query to update the email_group for all reports associated with from_email
        query = """
        UPDATE reports 
        SET email_group = %s 
        WHERE email_group = %s
        """

        # Execute the query to transfer the reports
        cursor.execute(query, (to_email, from_email))
        cnx.commit()  # Commit the transaction to save changes

        print(f"Transferring reports from {from_email} to {to_email}")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


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

        # Get report ID
        report_id_query = "SELECT id FROM reports WHERE email_group = %s AND year = %s"
        cursor.execute(report_id_query, (email_group, datetime.now().year))
        report_id = cursor.fetchone()[0]

        # Delete existing scheduled activities
        delete_scheduled_activities = "DELETE FROM scheduled_activities WHERE report_id = %s"
        cursor.execute(delete_scheduled_activities, (report_id,))

        # Insert or update scheduled activities
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

        # Handle unscheduled activities similarly
        delete_unscheduled_activities = "DELETE FROM unscheduled_activities WHERE report_id = %s"
        cursor.execute(delete_unscheduled_activities, (report_id,))

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
