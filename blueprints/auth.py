from flask import Blueprint, render_template, redirect, session, flash, request
from db.auth import *  # Importing the database module for user-related operations
from db.tutor import *  # Importing the database module for tutor-related operations

# Define the blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)

# Route for the home page, which redirects to the login page


@auth_bp.route("/")
def home():
    # Redirecting users to the login page when accessing the home route
    return redirect("/login")

# Route to display the login form


@auth_bp.route("/login", methods=["GET"])
def login_page():
    # Rendering the login form template
    return render_template("auth/login.html")

# Route to handle login form submissions


@auth_bp.route("/submit-login", methods=["POST"])
def submit_login():
    # Get the email and password from the form submission
    email = request.form.get("email")
    password = request.form.get("password")

    # Attempt to log the user in using the provided credentials
    user = login(email, password)

    if user:
        # If login is successful, store the user's email in the session
        session['email_user'] = user['email']

        # Check if the user is a CLA (Central Leadership Academy) member
        if claa_member(email):
            return redirect("/panel-claa")  # Redirect to the CLA member panel
        else:
            return redirect("/panel-tutor")  # Redirect to the tutor panel
    else:
        # If login fails, flash an error message and redirect to the login page
        flash("Login não realizado com sucesso - usuário não cadastrado ou senha incorreta")
        return redirect("/login")

# Route for handling different steps in the password recovery process


@auth_bp.route('/recover-password/<step>', methods=["GET"])
def recover_password_step(step):
    # Render the password recovery template and pass the current step
    return render_template("auth/recover-password.html", step=step)

# Route to handle sending the password recovery code


@auth_bp.route('/send-code', methods=["POST"])
def send_code_page():
    # Get the email from the form submission
    email = request.form.get("email")
    if user_exists(email):  # Check if the user exists in the database
        if send_code(email):  # Attempt to send the recovery code
            # Redirect to code entry step
            return redirect('/recover-password/code')
        else:
            # If sending the code fails, flash an error message
            flash("Falha ao enviar código para email")
            # Remove any existing code and email from the session
            session.pop('code', None)
            session.pop('email', None)
            # Redirect to email entry step
            return redirect('/recover-password/email')
    else:
        # Flash a message if the email is not registered
        flash("Email não cadastrado")
        return redirect('/recover-password/email')

# Route to verify the recovery code


@auth_bp.route('/verify-code', methods=["GET", "POST"])
def verify_code():
    if 'code' in session:  # Check if a code is stored in the session
        # Get the code from the form submission
        code = request.form.get("code")
        if code == session['code']:  # Check if the submitted code matches the session code
            # Redirect to password reset step
            return redirect('/recover-password/reset')
        else:
            # If the code is incorrect, flash an error message
            flash("Código inválido")
            # Redirect to code entry step
            return redirect('/recover-password/code')
    else:
        # Flash a message if no code has been sent
        flash("Código não enviado")
        # Redirect to email entry step
        return redirect('/recover-password/email')

# Route to handle password reset submissions


@auth_bp.route('/reset-password', methods=["POST", "GET"])
def reset_password_page():
    if 'email' in session:  # Check if an email is stored in the session
        # Get the new password from the form submission
        new_password = request.form.get("password")
        # Reset the password in the database
        reset_password(new_password)
        return redirect('/login')  # Redirect to the login page
    else:
        # Flash a message if no email is stored in the session
        flash("Email não cadastrado")
        # Remove any existing code and email from the session
        session.pop('code', None)
        session.pop('email', None)
        # Redirect to email entry step
        return redirect('/recover-password/email')

# Route to display the tutor signup form


@auth_bp.route("/signup-tutor", methods=["GET"])
def signup_tutor():
    # Render the signup form template
    return render_template("auth/signup-tutor.html")

# Route to handle tutor signup form submissions


@auth_bp.route("/submit-signup-tutor", methods=["POST"])
def submit_signup_tutor():
    # Get the form data
    name = request.form.get("name")
    status_claa = request.form.get("status-claa")
    email = request.form.get("email")
    password = request.form.get("password")

    # Check if the user already exists in the database
    if user_exists(email):
        # Flash an error message if the email is taken
        flash("Email já cadastrado. Por favor, tente novamente.")
        return redirect("/signup-tutor")  # Redirect back to the signup form
    else:
        # Insert the new tutor into the database
        insert_tutor(name, status_claa, email, password)
        # Redirect to the login page after successful signup
        return redirect("/login")

# Route to handle user logout


@auth_bp.route('/logout')
def logout():
    # Remove the user's email from the session to log them out
    session.pop('email_user', None)
    return redirect('/login')  # Redirect to the login page
