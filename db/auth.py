from flask import session
import mysql.connector
from mysql.connector import Error
import bcrypt
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db.config import config, smtp_server, smtp_port, smtp_username, smtp_password


def hash_password(password):
    """Hashes the password using bcrypt."""
    salt = bcrypt.gensalt()  # Generate a salt
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), salt)  # Hash the password
    # Return the hashed password as a string
    return hashed_password.decode('utf-8')


def login(email, password):
    """Authenticates the user by checking the hashed password against the stored hash."""
    try:
        # Establish a database connection
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # Query to get user details by email
        query = "SELECT name, email, password FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        # Ensure the cursor and connection are closed
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    if result is None:
        return False  # User not found

    stored_password = result['password']
    # Check if the provided password matches the stored hash
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        # Return user details on successful authentication
        user = {
            'name': result['name'],
            'email': result['email']
        }
        return user
    else:
        return False


def get_name_user_by_email(email):
    """Retrieves the user's name from the database using their email."""
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

    return result[0] if result else None  # Return the user's name if found


def claa_member(email):
    """Checks if a user is a member of CLAA and returns True if they are a holder or substitute."""
    if not user_exists(email):
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

    # Check if the user's status is 'holder' or 'substitute'
    if status_claa and status_claa[0] in ('holder', 'substitute'):
        return True
    else:
        return False


def user_exists(email):
    """Checks if a user exists in the database by email."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query = "SELECT 1 FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        user_exists = cursor.fetchone()

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return user_exists is not None


def send_signup_invitation(email):
    """Sends an invitation email for signing up as a tutor."""
    link = "http://127.0.0.1:5000/signup-tutor"  # Signup link

    sender_email = smtp_username
    subject = "Convite para se inscrever como Tutor"
    body = f"Você foi convidado para se inscrever como tutor. Clique no link para se inscrever: {link}"

    # Construct the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send the email using the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        print(f"Invitation sent to {email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_code(email):
    """Generates a random code and sends it to the user's email for password reset."""
    code = str(random.randint(100000, 999999)
               )  # Generate a random 6-digit code
    session['code'] = code
    session['email'] = email

    # Email content
    sender_email = smtp_username
    subject = "Your Password Reset Code"
    body = f"Your password reset code is: {code}"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        print(f"Code {code} sent to {email}")
        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def reset_password(new_password):
    """Resets the user's password using the provided new password."""
    email = session.get('email')

    if not email:
        print("Error: Email not found in session")
        return False

    try:
        # Hash the new password
        hashed_password = hash_password(new_password)

        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        # Update the user's password in the users table
        update_query = "UPDATE users SET password = %s WHERE email = %s"
        cursor.execute(update_query, (hashed_password, email))
        cnx.commit()

        # Clear the session
        session.pop('code', None)
        session.pop('email', None)

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return True


def get_all_users():
    """Fetches all users along with their associated group names."""
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(dictionary=True)

        # Fetch user data along with their associated group name
        query = """
        SELECT 
            users.email, 
            users.name, 
            users.status_claa,
            groups.name AS group_name
        FROM users
        LEFT JOIN claa.groups ON users.email = claa.groups.email_tutor
        """
        cursor.execute(query)
        users = cursor.fetchall()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

    return users
