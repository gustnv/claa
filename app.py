from flask import Flask, session, flash, render_template, redirect, request

from bd import bd


app = Flask(__name__)

# toda pagina em flask tem:
# route: caminho do site | / caminho default
# função: o que quer exibir na página

app.config["SECRET_KEY"] = "CLAA"  # replace with a security key


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
        session['name_user'] = user['name']
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
    session.pop('name_user', None)
    return redirect('/login')


@app.route("/panel-tutor", methods=["GET"])
def panel_tutor():
    if 'email_user' in session:
        name_tutor = session['name_user']

        report_exists = bd.report_exists(session['email_user'])

        tutor_has_group = bd.group_exists(session['email_user'])

        return render_template('panel-tutor.html', name_tutor=name_tutor,
                               tutor_has_group=tutor_has_group,
                               report_exists=report_exists)
    else:
        return redirect('/login')


@app.route("/panel-claa", methods=["GET"])
def panel_claa():
    if 'email_user' in session:
        name_claa = session['name_user']

        return render_template('panel-claa.html', name_claa=name_claa)
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
    return render_template("signup-group.html")


@ app.route("/submit-signup-group", methods=["POST"])
def submit_signup_group():
    name = request.form.get("name")
    email = request.form.get("email")
    insta = request.form.get("insta")
    page = request.form.get("page")
    nof_scholarships = request.form.get("nof-scholarships")
    nof_volunteers = request.form.get("nof-volunteers")
    address = request.form.get("address")
    campus = request.form.get("campus")
    center = request.form.get("center")

    if bd.group_exists(email):
        flash("Uncessuful registration - email already exists")
        return redirect("/signup-group")
    else:
        bd.insert_group(name, email, insta, page, nof_scholarships,
                        nof_volunteers, address, campus, center)
        return redirect("/panel-tutor")


@app.route("/add-group", methods=["GET"])
def add_group():
    return redirect("/signup-group")


@app.route("/edit-group", methods=["GET"])
def edit_group():
    return redirect("/signup-group")


@app.route("/add-report", methods=["GET"])
def add_report():
    return redirect("/report-0")


@app.route("/edit-report", methods=["GET"])
def edit_report():
    return redirect("/report-0")


@ app.route("/report-0", methods=["GET"])
def report_0():
    bd.reset_report_session()
    return render_template("report-0.html")


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
                "extension_hours": extension_hours or '0',
                "id": i
            }
            activities.append(activity)

    session['scheduled_activities'] = activities
    return redirect("/report-1")


@app.route("/report-1", methods=["GET"])
def report_1():
    return render_template("report-1.html")


@app.route("/submit-report-1", methods=["POST"])
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
                "extension_hours": extension_hours or '0',
                "id": i
            }
            activities.append(activity)

    session['unscheduled_activities'] = activities
    return redirect("/report-2")


@app.route("/report-2", methods=["GET"])
def report_2():
    return render_template("report-2.html")


@app.route("/submit-report-2", methods=["POST"])
def submit_report_2():
    session['activities_articulation'] = request.form.get(
        "activities-articulation")
    return redirect("/report-3")


@app.route("/report-3", methods=["GET"])
def report_3():
    return render_template("report-3.html")


@app.route("/submit-report-3", methods=["POST"])
def submit_report_3():
    session['politics_articulation'] = request.form.get(
        "politics-articulation")
    return redirect("/report-4")


@app.route("/report-4", methods=["GET"])
def report_4():
    return render_template("report-4.html")


@app.route("/submit-report-4", methods=["POST"])
def submit_report_4():
    session['selection_students'] = request.form.get("selection-students")
    return redirect("/report-5")


@app.route("/report-5", methods=["GET"])
def report_5():
    return render_template("report-5.html")


@app.route("/submit-report-5", methods=["POST"])
def submit_report_5():
    session['permanence_students'] = request.form.get("permanence-students")
    return redirect("/report-6")


@app.route("/report-6", methods=["GET"])
def report_6():
    return render_template("report-6.html")


@app.route("/submit-report-6", methods=["POST"])
def submit_report_6():
    session['ufsc_target_public'] = request.form.get("ufsc-target-public")
    session['society_target_public'] = request.form.get(
        "society-target-public")
    return redirect("/report-7")


@app.route("/report-7", methods=["GET"])
def report_7():
    return render_template("report-7.html")


@app.route("/submit-report-7", methods=["POST"])
def submit_report_7():
    session['infrastructure_condition'] = request.form.get(
        "infrastructure-condition")
    session['infrastructure_description'] = request.form.get(
        "infrastructure-description")
    return redirect("/report-8")


@app.route("/report-8", methods=["GET"])
def report_8():
    return render_template("report-8.html")


@app.route("/submit-report-8", methods=["POST"])
def submit_report_8():
    session['tools_condition'] = request.form.get("tools-condition")
    session['tools_description'] = request.form.get("tools-description")
    return redirect("/report-9")


@app.route("/report-9", methods=["GET"])
def report_9():
    return render_template("report-9.html")


@app.route("/submit-report-9", methods=["POST"])
def submit_report_9():
    session['costing_condition'] = request.form.get("costing-condition")
    session['costing_description'] = request.form.get("costing-description")
    return redirect("/submit-report")


@app.route("/submit-report", methods=["GET"])
def submit_report():
    bd.insert_report()

    return redirect("/panel-tutor")


if __name__ == "__main__":
    app.run(debug=True)
