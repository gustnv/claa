from flask import Flask, flash, render_template, redirect, request
from bd import bd


app = Flask(__name__)

# toda pagina em flask tem:
# route: caminho do site | / caminho default
# função: o que quer exibir na página

app.config["SECRET_KEY"] = "CLAA"


@app.route("/")
def home():
    return redirect("/signup-group")


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/submit-login", methods=["POST"])
def submit_login():
    email = request.form.get("email")
    password = request.form.get("password")

    user_authenticated = bd.login(email, password)

    if user_authenticated:
        return redirect("/panel")
    else:
        flash("Uncessuful login - user not registered or incorrect password")
        return redirect("/login")


@app.route("/signup-tutor", methods=["GET"])
def signup_tutor():
    return render_template("signup-tutor.html")


@app.route("/submit-signup-tutor", methods=["POST"])
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


@app.route("/signup-group", methods=["GET"])
def signup_group():
    return render_template("signup-group.html")


@app.route("/submit-signup-group", methods=["POST"])
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
        return redirect("/panel")


"""

dsfjadskjf

"""


@app.route("/report-2", methods=["GET"])
def report_2():
    return render_template("report-2.html")


@app.route("/submit-report-2", methods=["POST"])
def submit_report_2():
    activities_articulation = request.form.get("activities-articulation")
    bd.update_report(activities_articulation=activities_articulation)

    return redirect("/report-3")


@app.route("/report-3", methods=["GET"])
def report_3():
    return render_template("report-3.html")


@app.route("/submit-report-3", methods=["POST"])
def submit_report_3():
    politics_articulation = request.form.get("politics-articulation")
    bd.update_report(politics_articulation=politics_articulation)

    return redirect("/report-4")


@app.route("/report-4", methods=["get"])
def report_4():
    return render_template("report-4.html")


@ app.route("/submit-report-4", methods=["POST"])
def submit_report_4():
    selection_students = request.form.get("selection-students")
    bd.update_report(selection_students=selection_students)

    return redirect("/report-5")


@app.route("/report-5", methods=["GET"])
def report_5():
    return render_template("report-5.html")


@ app.route("/submit-report-5", methods=["POST"])
def submit_report_5():
    permanence_students = request.form.get("permanence-students")
    bd.update_report(permanence_students=permanence_students)

    return redirect("/report-6")


@app.route("/report-6", methods=["GET"])
def report_6():
    return render_template("report-6.html")


@ app.route("/submit-report-6", methods=["POST"])
def submit_report_6():
    ufsc_target_public = request.form.get("ufsc-target-public")
    bd.update_report(ufsc_target_public=ufsc_target_public)

    society_target_public = request.form.get("society-target-public")
    bd.update_report(society_target_public=society_target_public)

    return redirect("/report-7")


@app.route("/report-7", methods=["GET"])
def report_7():
    return render_template("report-7.html")


@ app.route("/submit-report-7", methods=["POST"])
def submit_report_7():
    infrastructure_condition = request.form.get("infrastructure-condition")
    bd.update_report(infrastructure_condition=infrastructure_condition)

    infrastructure_description = request.form.get("infrastructure-description")
    bd.update_report(infrastructure_description=infrastructure_description)

    return redirect("/report-8")


@app.route("/report-8", methods=["GET"])
def report_8():
    return render_template("report-8.html")


@ app.route("/submit-report-8", methods=["POST"])
def submit_report_8():
    tools_condition = request.form.get("tools-condition")
    bd.update_report(tools_condition=tools_condition)

    tools_description = request.form.get("tools-description")
    bd.update_report(tools_description=tools_description)

    return redirect("/report-9")


@app.route("/report-9", methods=["GET"])
def report_9():
    return render_template("report-9.html")


@ app.route("/submit-report-9", methods=["POST"])
def submit_report_9():
    costing_condition = request.form.get("costing-condition")
    bd.update_report(costing_condition=costing_condition)

    costing_description = request.form.get("costing-description")
    bd.update_report(costing_description=costing_description)

    bd.insert_report()

    return redirect("/panel")


@ app.route("/panel")
def panel():
    return render_template("panel.html")


if __name__ in "__main__":
    app.run(debug=True)
