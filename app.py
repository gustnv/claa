from flask import Flask, session, flash, render_template, redirect, request
from flask_session import Session
import os
from bd import bd

app = Flask(__name__)

# Configure Flask session
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "default_key")

# Use server-side session
# You can also use 'redis', 'memcached', 'sqlalchemy', etc.
app.config["SESSION_TYPE"] = "filesystem"  # session storage in sever side
app.config["SESSION_FILE_DIR"] = os.path.join(
    app.instance_path, 'flask_session')  # Directory to store session files
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True  # Adds an extra layer of security
Session(app)

config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'P4ssw0rd!'),
    'host': '127.0.0.1',
    'database': 'claa',
    'raise_on_warnings': True
}


@app.route("/")
def home():
    return redirect("/signup-tutor")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/submit-login", methods=["POST"])
def submit_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = bd.login(email, password)

    if user:
        session['email_user'] = user['email']

        if bd.claa_member(email):
            return redirect("/panel-claa")
        else:
            return redirect("/panel-tutor")
    else:
        flash("Uncessuful login - user not registered or incorrect password")
        return redirect("/login")


@app.route('/logout')
def logout():
    session.pop('email_user', None)
    return redirect('/login')


@app.route("/panel-tutor", methods=["GET"])
def panel_tutor():
    if 'email_user' in session:
        bd.reset_session()

        email_group = bd.get_email_group_by_tutor(session['email_user'])
        report_exists = bd.report_exists(email_group)

        tutor_has_group = bd.get_group_by_email_tutor(session['email_user'])

        return render_template('panel-tutor.html', name_tutor=bd.get_name_user_by_email(session['email_user']),
                               tutor_has_group=tutor_has_group,
                               report_exists=report_exists)
    else:
        return redirect('/login')


@app.route("/panel-claa", methods=["GET"])
def panel_claa():
    if 'email_user' in session:
        return render_template('panel-claa.html', name_claa=bd.get_name_user_by_email(session['email_user']))
    else:
        return redirect('/login')


@ app.route("/signup-tutor", methods=["GET"])
def signup_tutor():
    return render_template("signup-tutor.html")


@ app.route("/submit-signup-tutor", methods=["POST"])
def submit_signup_tutor():
    name = request.form.get("name")
    status_claa = request.form.get("status-claa")
    email = request.form.get("email")
    password = request.form.get("password")

    if bd.tutor_exists(email):
        flash("Uncessuful registration - email already exists")
        return redirect("/signup-tutor")
    else:
        bd.insert_tutor(name, status_claa, email, password)
        return redirect("/login")


@ app.route("/signup-group", methods=["GET"])
def signup_group():
    # Check for tutor email in session
    email_tutor = session.get("email_user")
    if not email_tutor:
        # Store form data in session
        return redirect("/login")

    form_data = session.get('signup_group_data', {})

    session.pop('signup_group_data', None)

    return render_template("signup-group.html", form_data=form_data)


@ app.route("/submit-signup-group", methods=["POST", "GET"])
def submit_signup_group():
    # Retrieve form data
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
    session['signup_group_data'] = form_data

    # Check for tutor email in session
    email_tutor = session.get("email_user")
    if not email_tutor:
        # Store form data in session
        return redirect("/login")

    if bd.get_group_by_email_tutor(email_tutor):
        bd.update_group(form_data, email_tutor)
        return redirect("/panel-tutor")
    else:
        # Proceed if email is found
        if bd.group_exists(form_data["email"]):
            flash("Unsuccessful registration - email already exists")
            return redirect("/signup-group")
        else:
            bd.insert_group(form_data, email_tutor=email_tutor)
            return redirect("/panel-tutor")


@ app.route("/add-group", methods=["GET"])
def add_group():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    return redirect("/signup-group")


@ app.route("/edit-group", methods=["GET"])
def edit_group():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    group_data = bd.get_group_by_email_tutor(email_tutor)

    if group_data:
        # Store fetched group data in session
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

    return redirect("/signup-group")


@ app.route("/add-report", methods=["GET"])
def add_report():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    return redirect("/report-0")


@ app.route("/edit-report", methods=["GET"])
def edit_report():
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    # Fetch existing report data if available
    email_group = bd.get_email_group_by_tutor(email_tutor)

    report_data = bd.get_report_by_email_group(email_group)
    report_id = report_data[0]
    if report_data:
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

    scheduled_activities = bd.get_scheduled_activities(report_id)
    if scheduled_activities:
        session['scheduled_activities'] = scheduled_activities

    unscheduled_activities = bd.get_unscheduled_activities(report_id)
    if unscheduled_activities:
        session['unscheduled_activities'] = unscheduled_activities

    return redirect("/report-0")


@ app.route("/report-0", methods=["GET"])
def report_0():
    scheduled_activities = session.get('scheduled_activities', [])
    return render_template("report-0.html", scheduled_activities=scheduled_activities)


@ app.route("/submit-report-0", methods=["POST"])
def submit_report_0():
    activities = []

    for i in range(100):
        name = request.form.get(f"name-{i}")
        carrying_out = request.form.get(f"carrying-out-{i}")
        total_hours = request.form.get(f"total-hours-{i}")
        teaching_hours = request.form.get(f"teaching-hours-{i}")
        research_hours = request.form.get(f"research-hours-{i}")
        extension_hours = request.form.get(f"extension-hours-{i}")

        if name:
            activity = {
                "name": name,
                "carrying_out": carrying_out,
                "total_hours": total_hours,
                "teaching_hours": teaching_hours or '0',
                "research_hours": research_hours or '0',
                "extension_hours": extension_hours or '0'
            }
            activities.append(activity)

    session['scheduled_activities'] = activities

    return redirect("/report-1")


@ app.route("/report-1", methods=["GET"])
def report_1():
    unscheduled_activities = session.get('unscheduled_activities', [])
    return render_template("report-1.html", unscheduled_activities=unscheduled_activities)


@ app.route("/submit-report-1", methods=["POST"])
def submit_report_1():
    activities = []

    for i in range(100):
        name = request.form.get(f"name-{i}")
        justification = request.form.get(f"justification-{i}")
        total_hours = request.form.get(f"total-hours-{i}")
        teaching_hours = request.form.get(f"teaching-hours-{i}")
        research_hours = request.form.get(f"research-hours-{i}")
        extension_hours = request.form.get(f"extension-hours-{i}")

        if name:
            activity = {
                "name": name,
                "justification": justification,
                "total_hours": total_hours,
                "teaching_hours": teaching_hours or '0',
                "research_hours": research_hours or '0',
                "extension_hours": extension_hours or '0'
            }
            activities.append(activity)

    session['unscheduled_activities'] = activities

    return redirect("/report-2")


@ app.route("/report-2", methods=["GET"])
def report_2():
    return render_template("report-2.html", activities_articulation=session.get('activities_articulation', ''))


@ app.route("/submit-report-2", methods=["POST"])
def submit_report_2():
    session['activities_articulation'] = request.form.get(
        "activities-articulation")

    return redirect("/report-3")


@ app.route("/report-3", methods=["GET"])
def report_3():
    return render_template("report-3.html", politics_articulation=session.get('politics_articulation', ''))


@ app.route("/submit-report-3", methods=["POST"])
def submit_report_3():
    session['politics_articulation'] = request.form.get(
        "politics-articulation")

    return redirect("/report-4")


@ app.route("/report-4", methods=["GET"])
def report_4():
    return render_template("report-4.html", selection_students=session.get('selection_students', ''))


@ app.route("/submit-report-4", methods=["POST"])
def submit_report_4():
    session['selection_students'] = request.form.get("selection-students")

    return redirect("/report-5")


@ app.route("/report-5", methods=["GET"])
def report_5():
    return render_template("report-5.html", permanence_students=session.get('permanence_students', ''))


@ app.route("/submit-report-5", methods=["POST"])
def submit_report_5():
    session['permanence_students'] = request.form.get("permanence-students")

    return redirect("/report-6")


@ app.route("/report-6", methods=["GET"])
def report_6():
    return render_template("report-6.html",
                           ufsc_target_public=session.get(
                               'ufsc_target_public', ''),
                           society_target_public=session.get(
                               'society_target_public', '')
                           )


@ app.route("/submit-report-6", methods=["POST"])
def submit_report_6():
    session['ufsc_target_public'] = request.form.get("ufsc-target-public")
    session['society_target_public'] = request.form.get(
        "society-target-public")

    return redirect("/report-7")


@ app.route("/report-7", methods=["GET"])
def report_7():
    return render_template("report-7.html",
                           infrastructure_condition=session.get(
                               'infrastructure_condition', ''),
                           infrastructure_description=session.get(
                               'infrastructure_description', '')
                           )


@ app.route("/submit-report-7", methods=["POST"])
def submit_report_7():
    session['infrastructure_condition'] = request.form.get(
        "infrastructure-condition")
    session['infrastructure_description'] = request.form.get(
        "infrastructure-description")

    return redirect("/report-8")


@ app.route("/report-8", methods=["GET"])
def report_8():
    return render_template("report-8.html",
                           tools_condition=session.get('tools_condition', ''),
                           tools_description=session.get(
                               'tools_description', '')
                           )


@ app.route("/submit-report-8", methods=["POST"])
def submit_report_8():
    session['tools_condition'] = request.form.get("tools-condition")
    session['tools_description'] = request.form.get("tools-description")

    return redirect("/report-9")


@ app.route("/report-9", methods=["GET"])
def report_9():
    return render_template("report-9.html",
                           costing_condition=session.get(
                               'costing_condition', ''),
                           costing_description=session.get(
                               'costing_description', '')
                           )


@ app.route("/submit-report-9", methods=["POST"])
def submit_report_9():
    session['costing_condition'] = request.form.get("costing-condition")
    session['costing_description'] = request.form.get("costing-description")

    return redirect("/submit-report")


@ app.route("/submit-report", methods=["GET"])
def submit_report():
    # Check for tutor email in session
    email_tutor = session.get("email_user")
    if not email_tutor:
        return redirect("/login")

    email_group = bd.get_email_group_by_tutor(session['email_user'])
    if bd.report_exists(email_group):
        bd.update_report(email_group)
    else:
        bd.insert_report(email_group)

    return redirect("/panel-tutor")


if __name__ == "__main__":
    app.run(debug=True)
