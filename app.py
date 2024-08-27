from flask import Flask, flash, render_template, redirect, request
from bd import bd


app = Flask(__name__)

# toda pagina em flask tem:
# route: caminho do site | / caminho default
# função: o que quer exibir na página

app.config["SECRET_KEY"] = "CLAA"


@app.route("/")
def home():
    return render_template("report-1.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user_authenticated = bd.login(email, password)

    if not user_authenticated:
        flash("Uncessuful login - user not registered or incorrect password")
        print("\nUsuário não cadastrado ou senha incorreta\n")
        return render_template("login.html")
    else:
        print("\nUsuário autenticado com sucesso\n")
        return redirect("/panel")


@app.route("/signup-tutor", methods=["POST"])
def signup_tutor():
    name = request.form.get("name")
    status_claa = request.form.get("status-claa")
    email = request.form.get("email")
    password = request.form.get("password")

    if bd.tutor_exists(email):
        flash("Uncessuful registration - email already exists")
    else:
        bd.insert_tutor(name, status_claa, email, password)

    return render_template("signup-tutor.html")


@app.route("/signup-group", methods=["POST"])
def signup_group_page():
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
    else:
        bd.insert_group(name, email, insta, page, nof_scholarships,
                        nof_volunteers, address, campus, center)

    return render_template("signup-group.html")


@app.route("/report-0")
def report0_page():
    return render_template("report-0.html")


@app.route("/report-1")
def report1_page():
    return render_template("report-1.html")


@app.route("/report-2")
def report2_page():
    return render_template("report-2.html")


@app.route("/report-3")
def report3_page():
    return render_template("report-3.html")


@app.route("/report-4")
def report4_page():
    return render_template("report-4.html")


@app.route("/report-5")
def report5_page():
    return render_template("report-5.html")


@app.route("/report-6")
def report6_page():
    return render_template("report-6.html")


@app.route("/report-7")
def report7_page():
    return render_template("report-7.html")


@app.route("/report-8")
def report8_page():
    return render_template("report-8.html")


@app.route("/report-9")
def report9_page():
    return render_template("report-9.html")


@app.route("/panel")
def panel_page():
    return render_template("panel.html")


@app.route("/profile")
def profile_page():
    return render_template("profile.html")


if __name__ in "__main__":
    app.run(debug=True)
