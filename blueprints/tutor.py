from flask import Blueprint, render_template, redirect, session, flash, request
# Importing the database module for interacting with group and tutor data
from db.auth import *
from db.group import *
from db.report import *

# Define the blueprint for tutor-related routes
tutor_bp = Blueprint('group', __name__)

# Route to display the tutor panel


@tutor_bp.route("/panel-tutor", methods=["GET"])
def panel_tutor():
    if 'email_user' in session:
        # Fetch the group email associated with the logged-in tutor
        email_group = get_email_group_by_tutor(session['email_user'])
        # Check if a report exists for the tutor's group
        report_bool = report_exists(email_group)
        # Check if the tutor has an associated group
        tutor_has_group = get_group_by_email_tutor(
            session['email_user'])
        print("ok")

        # Render the tutor panel with the relevant information
        return render_template('tutor/panel-tutor.html',
                               name_tutor=get_name_user_by_email(
                                   session['email_user']),
                               tutor_has_group=tutor_has_group,
                               report_exists=report_bool)
    else:
        # Redirect to login if the user is not logged in
        return redirect('/login')

# Route to display the group signup form


@tutor_bp.route("/signup-group", methods=["GET"])
def signup_group():
    # Check for tutor email in session
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Retrieve any previously saved form data from the session
    form_data = session.get('signup_group_data', {})

    # Remove the saved form data from the session after fetching it
    session.pop('signup_group_data', None)

    # Render the group signup form with the retrieved form data
    return render_template("tutor/signup-group.html", form_data=form_data)

# Route to handle the submission of the group signup form


@tutor_bp.route("/submit-signup-group", methods=["POST", "GET"])
def submit_signup_group():
    # Retrieve form data from the request
    form_data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "insta": request.form.get("insta"),
        "page": request.form.get("page"),
        "nof_scholarships": request.form.get("nof-scholarships"),
        "nof_volunteers": request.form.get("nof-volunteers"),
        "address": request.form.get("address"),
        "campus": request.form.get("campus"),
        "center": request.form.get("center"),
    }
    # Save the form data in session in case of errors or redirection
    session['signup_group_data'] = form_data

    # Check for tutor email in session
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Check if the tutor already has a group
    if get_group_by_email_tutor(email_tutor):
        # Update the group details if the tutor already has a group
        print(get_group_by_email_tutor(form_data["email"]))
        if group_exists(form_data["email"]) and get_group_by_email_tutor(email_tutor)[0] != form_data["email"]:
            flash("Email indisponível - pertence a outro grupo")
            return redirect("/signup-group")

            # Update the group details if the tutor already has a group
        update_group(form_data, email_tutor)
        session.pop('signup_group_data', None)  # Clear saved form data
        return redirect("/panel-tutor")
    else:
        if group_exists(form_data["email"]):
            # Flash message for duplicate group email
            flash("Registro não realizado com sucesso - email já utilizado")
            # Redirect back to the signup form
            return redirect("/signup-group")
        # Insert a new group if it doesn't already exist
        insert_group(form_data, email_tutor=email_tutor)
        session.pop('signup_group_data', None)  # Clear saved form data
        return redirect("/panel-tutor")

# Route to add a new group for the tutor


@tutor_bp.route("/add-group", methods=["GET"])
def add_group():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Redirect to the group signup form
    return redirect("/signup-group")

# Route to edit an existing group for the tutor


@tutor_bp.route("/edit-group", methods=["GET"])
def edit_group():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Fetch the group data associated with the tutor
    group_data = get_group_by_email_tutor(email_tutor)

    if group_data:
        # Store the fetched group data in the session to pre-fill the form
        session['signup_group_data'] = {
            "email": group_data[0],
            "name": group_data[1],
            "insta": group_data[2],
            "page": group_data[3],
            "nof_scholarships": group_data[4],
            "nof_volunteers": group_data[5],
            "address": group_data[6],
            "campus": group_data[7],
            "center": group_data[8]
        }

    # Redirect to the group signup form with pre-filled data
    return redirect("/signup-group")
