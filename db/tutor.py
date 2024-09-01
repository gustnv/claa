import mysql.connector
from mysql.connector import Error
from db.config import config
from db.auth import hash_password

# Function to insert a new tutor into the users table


def insert_tutor(name, status_claa, email, password):
    try:
        # Establish a connection to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # SQL query to insert a new user
        query = (
            "INSERT INTO users (name, status_claa, email, password) VALUES (%s, %s, %s, %s)"
        )

        # Hash the password for security
        hashed_password = hash_password(password)
        data = (name, status_claa, email, hashed_password)

        # Execute the query with the provided data
        cursor.execute(query, data)
        cnx.commit()  # Commit the changes to the database

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Ensure cursor and connection are closed to avoid resource leaks
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

# Function to retrieve all tutors who are not associated with any group


def get_tutors_without_group():
    try:
        # Establish a connection to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # SQL query to get users without a group
        query = """
        SELECT users.email, users.name 
        FROM users 
        LEFT JOIN claa.groups ON users.email = claa.groups.email_tutor 
        WHERE claa.groups.email_tutor IS NULL
        """
        cursor.execute(query)
        tutors = cursor.fetchall()  # Fetch all results

    except Error as e:
        print(f"Error: {e}")
        return []

    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return tutors

# Function to check if a tutor is associated with any group


def tutor_has_group(email):
    try:
        # Establish a connection to the database
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # SQL query to check if the tutor has a group
        query = "SELECT 1 FROM claa.groups WHERE email_tutor = %s"
        cursor.execute(query, (email,))
        tutor_has_group = cursor.fetchone()  # Fetch the result

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        # Ensure cursor and connection are closed
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return tutor_has_group is not None

# Function to delete a tutor from the database


def delete_tutor(email):
    # Check if the tutor is not associated with any group
    if not tutor_has_group(email):
        try:
            # Establish a connection to the database
            cnx = mysql.connector.connect(**config)
            cursor = cnx.cursor()

            # SQL query to delete the tutor
            query = "DELETE FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            cnx.commit()  # Commit the changes to the database

            return True

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            return False

        finally:
            # Ensure cursor and connection are closed
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
    else:
        # Return False if the tutor is associated with a group
        return False
