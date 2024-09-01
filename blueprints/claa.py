from flask import Blueprint, render_template, redirect, session, flash, request
# Import the database module for interacting with tutor and group data
from db.auth import *
from db.group import *
from db.tutor import *

# Define the blueprint for CLAA-related routes
claa_bp = Blueprint('claa', __name__)

# Route to display the CLAA panel


@claa_bp.route("/panel-claa", methods=["GET"])
def panel_claa():
    if 'email_user' in session:
        # Render the CLAA panel with the user's name fetched from the database
        return render_template('claa/panel-claa.html', name_claa=get_name_user_by_email(session['email_user']))
    else:
        # Redirect to login if the user is not logged in
        return redirect('/login')

# Route to display the group transfer page


@claa_bp.route("/transfer-group", methods=["GET"])
def transfer_group_page():
    email_tutor = session.get("email_user")
    if not email_tutor:
        # Redirect to login if the tutor is not logged in
        return redirect("/login")

    # Fetch all groups and tutors without a group from the database
    groups = get_all_groups()
    tutors_without_group = get_tutors_without_group()

    # Render the group transfer page with the list of groups and available tutors
    return render_template("claa/transfer-group.html", groups=groups, tutors_without_group=tutors_without_group)

# Route to handle the submission of a group transfer


@claa_bp.route("/submit-transfer-group", methods=["POST"])
def submit_transfer_group():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Get the selected group and tutor emails from the form
    group_email = request.form.get("group-email")
    tutor_email = request.form.get("tutor-email")

    # Check if the selected tutor already belongs to a group
    if tutor_has_group(tutor_email):
        # Display a flash message if the tutor already has a group
        flash("Tutor já pertence a um grupo.")
        # Redirect back to the transfer page
        return redirect("/transfer-group")

    # Transfer the group to the selected tutor
    transfer_group(group_email, tutor_email)
    return redirect("/panel-claa")  # Redirect to the CLAA panel after transfer

# Route to display the tutor management page


@claa_bp.route("/tutor", methods=["GET"])
def tutor_page():
    if 'email_user' in session:
        # Fetch all users (tutors) from the database
        users = get_all_users()

        for user in users:
            if user['email'] == session['email_user']:
                users.remove(user)
                break

        # Render the tutor management page with the user list
        return render_template('claa/tutor.html', users=users)
    else:
        return redirect('/login')

# Route to delete a tutor based on their email


@claa_bp.route("/delete-tutor/<email>", methods=["DELETE"])
def delete_tutor_page(email):
    # Attempt to delete the tutor from the database
    print(email)
    if delete_tutor(email):
        # Return a success response if deletion is successful
        return {"success": True}, 200
    else:
        # Return an error message if deletion fails
        return {"success": False, "message": "Falha ao remover tutor."}, 400

# Route to handle the invitation of a new tutor


@claa_bp.route("/invite-tutor", methods=["POST"])
def invite_tutor():
    email = request.form.get("email")  # Get the email from the form submission

    # Check if the user already exists in the system
    if user_exists(email):
        # Flash message if email is already registered
        flash("Email já cadastrado. Por favor, tente novamente.")
    else:
        # Send a signup invitation to the provided email
        if not send_signup_invitation(email):
            # Flash message if invitation fails
            flash("Falha ao enviar convite para email.")

    return redirect('/tutor')  # Redirect back to the tutor management page
