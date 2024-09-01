import mysql.connector
from mysql.connector import Error
from db.config import config


def get_group_by_email_tutor(email_tutor):
    """Fetches a group from the database using the tutor's email."""
    try:
        # Establish a database connection
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Query to select the group based on the tutor's email
        query = "SELECT * FROM claa.groups WHERE email_tutor = %s"
        cursor.execute(query, (email_tutor,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return result


def group_exists(email):
    """Checks if a group exists in the database using the email."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Query to check if a group exists with the given email
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

    return group_exists is not None  # Return True if a group exists, False otherwise


def update_group(form_data, email_tutor):
    """Updates a group's details in the database using the provided form data."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Step 1: Fetch the current email associated with the tutor
        current_email = get_email_group_by_tutor(email_tutor)

        # Step 2: Transfer the report to the new email (if email is being changed)
        if current_email != form_data["email"]:
            # Set reports.email_group to NULL where email_group = current_email
            query_set_null = """
            UPDATE claa.reports
            SET email_group = NULL
            WHERE email_group = %s
            """
            cursor.execute(query_set_null, (current_email,))
            cnx.commit()  # Commit the transaction to save chan

            # Query to update the group details
        query = """
        UPDATE claa.groups 
        SET email = %s, name = %s, instagram = %s, webpage = %s, nof_scholarships = %s,
            nof_volunteers = %s, address = %s, campus = %s, center = %s
        WHERE email_tutor = %s
        """

        # Execute the query with the form data
        cursor.execute(query, (
            form_data['email'],
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
        cnx.commit()  # Commit the transaction to save changes

        # Step 4: Set the email_group in reports table to the new email where it is NULL
        query_update_reports = """
        UPDATE claa.reports
        SET email_group = %s
        WHERE email_group IS NULL
        """
        cursor.execute(query_update_reports,
                       (form_data['email'],))
        cnx.commit()  # Commit the transaction to save changes

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def insert_group(form_data, email_tutor):
    """Inserts a new group into the database using the provided form data."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Query to insert a new group
        query = (
            "INSERT INTO claa.groups "
            "(name, email, instagram, webpage, nof_scholarships, nof_volunteers, "
            "address, campus, center, email_tutor) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        # Data to be inserted
        data = (
            form_data['name'], form_data['email'], form_data['insta'],
            form_data['page'], form_data['nof_scholarships'], form_data['nof_volunteers'],
            form_data['address'], form_data['campus'], form_data['center'], email_tutor
        )

        cursor.execute(query, data)  # Execute the query with the provided data
        cnx.commit()  # Commit the transaction to save changes

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


def get_email_group_by_tutor(email_tutor):
    """Fetches the email associated with a group from the database using the tutor's email."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Query to select the group's email based on the tutor's email
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

    return result[0] if result else None  # Return the group's email if found


def get_all_groups():
    """Fetches all groups from the database."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # Query to select all groups
        query = "SELECT * FROM claa.groups"
        cursor.execute(query)
        groups = cursor.fetchall()  # Fetch all groups

    except Error as e:
        print(f"Error: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return groups


def transfer_group(group_email, tutor_email):
    """Transfers a group to a new tutor by updating the tutor's email in the database."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Query to update the group with the new tutor's email
        query = "UPDATE claa.groups SET email_tutor = %s WHERE email = %s"
        cursor.execute(query, (tutor_email, group_email))
        cnx.commit()  # Commit the transaction to save changes

    except Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()
