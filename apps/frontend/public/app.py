from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)

# Set the necessary configurations before initializing SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'password'

db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    email = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    status_claa = db.Column(db.String(0), nullable=False)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/panel')
def panel():
    return render_template('panel.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/recover-code')
def recover_code():
    return render_template('recover-code.html')


@app.route('/recover-email')
def recover_email():
    return render_template('recover-email.html')


@app.route('/recover-password')
def recover_password():
    return render_template('recover-password.html')


@app.route('/report-0')
def report_0():
    return render_template('report-0.html')


@app.route('/report-1')
def report_1():
    return render_template('report-1.html')


@app.route('/report-2')
def report_2():
    return render_template('report-2.html')


@app.route('/report-3')
def report_3():
    return render_template('report-3.html')


@app.route('/report-4')
def report_4():
    return render_template('report-4.html')


@app.route('/report-5')
def report_5():
    return render_template('report-5.html')


@app.route('/report-6')
def report_6():
    return render_template('report-6.html')


@app.route('/report-7')
def report_7():
    return render_template('report-7.html')


@app.route('/report-8')
def report_8():
    return render_template('report-8.html')


@app.route('/report-9')
def report_9():
    return render_template('report-9.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/tutor')
def tutor():
    return render_template('tutor.html')


if __name__ == '__main__':
    app.run(debug=True)
