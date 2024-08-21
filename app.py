from flask import Flask, render_template, redirect, request


app = Flask(__name__)

# toda pagina em flask tem:
# route: caminho do site | / caminho default
# função: o que quer exibir na página

@app.route('/')
def login_page():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    senha = request.form.get("senha")
    print(email)
    print(senha)
    return redirect('/')


@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/panel")
def panel_page():
    return render_template("panel.html")

@app.route("/profile")
def profile_page():
    return render_template("profile.html")

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

if __name__ in "__main__":
    app.run(debug=True)