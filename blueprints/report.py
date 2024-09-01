from flask import Blueprint, render_template, redirect, session, request
# Importing the database module for interacting with report data
from db.group import *
from db.report import *

# Define the blueprint for report-related routes
report_bp = Blueprint('report', __name__)

# Route to start the process of adding a report


@report_bp.route("/add-report", methods=["GET"])
def add_report():
    email_tutor = session.get("email_user")  # Check if a tutor is logged in
    if not email_tutor:
        return redirect("/login")  # Redirect to login if no tutor is logged in

    reset_report_session()

    return redirect("/report-0")  # Start at the first report step

# Route to edit an existing report


@report_bp.route("/edit-report", methods=["GET"])
def edit_report():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Fetch the group email associated with the logged-in tutor
    email_group = get_email_group_by_tutor(email_tutor)

    # Fetch existing report data if available
    report_data = get_report_by_email_group(email_group)
    if report_data:
        # Save report data into session for editing
        report_id = report_data[0]
        session['activities_articulation'] = report_data[1]
        session['politics_articulation'] = report_data[2]
        session['selection_students'] = report_data[3]
        session['permanence_students'] = report_data[4]
        session['ufsc_target_public'] = report_data[5]
        session['society_target_public'] = report_data[6]
        session['infrastructure_condition'] = report_data[7]
        session['infrastructure_description'] = report_data[8]
        session['tools_condition'] = report_data[9]
        session['tools_description'] = report_data[10]
        session['costing_condition'] = report_data[11]
        session['costing_description'] = report_data[12]

    # Fetch scheduled and unscheduled activities associated with the report
    scheduled_activities = get_scheduled_activities(report_id)
    if scheduled_activities:
        session['scheduled_activities'] = scheduled_activities

    unscheduled_activities = get_unscheduled_activities(report_id)
    if unscheduled_activities:
        session['unscheduled_activities'] = unscheduled_activities

    return redirect("/report-0")  # Redirect to the first step for editing

# Route to display the first report step, showing scheduled activities


@report_bp.route("/report-0", methods=["GET"])
def report_0():
    scheduled_activities = session.get('scheduled_activities', [])
    return render_template("report/report-0.html", scheduled_activities=scheduled_activities)

# Route to handle the submission of the first report step


@report_bp.route("/submit-report-0", methods=["POST"])
def submit_report_0():
    activities = []

    # Collect up to 100 scheduled activities from the form
    for i in range(100):
        name = request.form.get(f"name-{i}")
        carrying_out = request.form.get(f"carrying-out-{i}")
        total_hours = request.form.get(f"total-hours-{i}")
        teaching_hours = request.form.get(f"teaching-hours-{i}")
        research_hours = request.form.get(f"research-hours-{i}")
        extension_hours = request.form.get(f"extension-hours-{i}")

        if name:
            # Store the collected data in a dictionary
            activity = {
                "name": name,
                "carrying_out": carrying_out,
                "total_hours": total_hours,
                "teaching_hours": teaching_hours or '0',
                "research_hours": research_hours or '0',
                "extension_hours": extension_hours or '0'
            }
            activities.append(activity)

    # Save the scheduled activities to the session
    session['scheduled_activities'] = activities

    return redirect("/report-1")  # Proceed to the next step

# Route to display the second report step, showing unscheduled activities


@report_bp.route("/report-1", methods=["GET"])
def report_1():
    unscheduled_activities = session.get('unscheduled_activities', [])
    return render_template("report/report-1.html", unscheduled_activities=unscheduled_activities)

# Route to handle the submission of the second report step


@report_bp.route("/submit-report-1", methods=["POST"])
def submit_report_1():
    activities = []

    # Collect up to 100 unscheduled activities from the form
    for i in range(100):
        name = request.form.get(f"name-{i}")
        justification = request.form.get(f"justification-{i}")
        total_hours = request.form.get(f"total-hours-{i}")
        teaching_hours = request.form.get(f"teaching-hours-{i}")
        research_hours = request.form.get(f"research-hours-{i}")
        extension_hours = request.form.get(f"extension-hours-{i}")

        if name:
            # Store the collected data in a dictionary
            activity = {
                "name": name,
                "justification": justification,
                "total_hours": total_hours,
                "teaching_hours": teaching_hours or '0',
                "research_hours": research_hours or '0',
                "extension_hours": extension_hours or '0'
            }
            activities.append(activity)

    # Save the unscheduled activities to the session
    session['unscheduled_activities'] = activities

    return redirect("/report-2")  # Proceed to the next step

# Routes for each subsequent report step


@report_bp.route("/report-2", methods=["GET"])
def report_2():
    return render_template("report/report-2.html", activities_articulation=session.get('activities_articulation', ''))


@report_bp.route("/submit-report-2", methods=["POST"])
def submit_report_2():
    session['activities_articulation'] = request.form.get(
        "activities-articulation")
    return redirect("/report-3")


@report_bp.route("/report-3", methods=["GET"])
def report_3():
    return render_template("report/report-3.html", politics_articulation=session.get('politics_articulation', ''))


@report_bp.route("/submit-report-3", methods=["POST"])
def submit_report_3():
    session['politics_articulation'] = request.form.get(
        "politics-articulation")
    return redirect("/report-4")


@report_bp.route("/report-4", methods=["GET"])
def report_4():
    return render_template("report/report-4.html", selection_students=session.get('selection_students', ''))


@report_bp.route("/submit-report-4", methods=["POST"])
def submit_report_4():
    session['selection_students'] = request.form.get("selection-students")
    return redirect("/report-5")


@report_bp.route("/report-5", methods=["GET"])
def report_5():
    return render_template("report/report-5.html", permanence_students=session.get('permanence_students', ''))


@report_bp.route("/submit-report-5", methods=["POST"])
def submit_report_5():
    session['permanence_students'] = request.form.get("permanence-students")
    return redirect("/report-6")


@report_bp.route("/report-6", methods=["GET"])
def report_6():
    return render_template("report/report-6.html",
                           ufsc_target_public=session.get(
                               'ufsc_target_public', ''),
                           society_target_public=session.get(
                               'society_target_public', '')
                           )


@report_bp.route("/submit-report-6", methods=["POST"])
def submit_report_6():
    session['ufsc_target_public'] = request.form.get("ufsc-target-public")
    session['society_target_public'] = request.form.get(
        "society-target-public")
    return redirect("/report-7")


@report_bp.route("/report-7", methods=["GET"])
def report_7():
    return render_template("report/report-7.html",
                           infrastructure_condition=session.get(
                               'infrastructure_condition', ''),
                           infrastructure_description=session.get(
                               'infrastructure_description', '')
                           )


@report_bp.route("/submit-report-7", methods=["POST"])
def submit_report_7():
    session['infrastructure_condition'] = request.form.get(
        "infrastructure-condition")
    session['infrastructure_description'] = request.form.get(
        "infrastructure-description")
    return redirect("/report-8")


@report_bp.route("/report-8", methods=["GET"])
def report_8():
    return render_template("report/report-8.html",
                           tools_condition=session.get('tools_condition', ''),
                           tools_description=session.get(
                               'tools_description', '')
                           )


@report_bp.route("/submit-report-8", methods=["POST"])
def submit_report_8():
    session['tools_condition'] = request.form.get("tools-condition")
    session['tools_description'] = request.form.get("tools-description")
    return redirect("/report-9")


@report_bp.route("/report-9", methods=["GET"])
def report_9():
    return render_template("report/report-9.html",
                           costing_condition=session.get(
                               'costing_condition', ''),
                           costing_description=session.get(
                               'costing_description', '')
                           )


@report_bp.route("/submit-report-9", methods=["POST"])
def submit_report_9():
    session['costing_condition'] = request.form.get("costing-condition")
    session['costing_description'] = request.form.get("costing-description")
    return redirect("/submit-report")

# Final route to submit the complete report


@report_bp.route("/submit-report", methods=["GET"])
def submit_report():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    email_group = get_email_group_by_tutor(email_tutor)

    # Check if the report already exists; if so, update it; otherwise, insert a new report
    if report_exists(email_group):
        update_report(email_group)
    else:
        insert_report(email_group)

    # Clear session data after submission
    reset_report_session()
    # Redirect to the tutor panel after submission
    return redirect("/panel-tutor")
