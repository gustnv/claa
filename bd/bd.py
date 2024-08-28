import mysql.connector
import bcrypt
from datetime import datetime

config = {
    'user': 'root',
    'password': 'P4ssw0rd!',
    'host': '127.0.0.1',
    'database': 'claa',
    'raise_on_warnings': True
}


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def login(email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = "select password from tutors where email = %s"
    cursor.execute(query, (email, ))

    result = cursor.fetchone()
    cursor.close()
    cnx.close()

    if result is None:
        return False

    stored_password = result[0]
    if bcrypt.checkpw(password.encode('utf-8'),
                      stored_password.encode('utf-8')):
        return True
    else:
        return False


def tutor_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from tutors where email = %s")
    cursor.execute(query, (email, ))
    tutor_exists = cursor.fetchone()

    cursor.close()
    cnx.close()

    if tutor_exists is None:
        return False
    else:
        return True


def insert_tutor(name, status_claa, email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "insert into tutors (name, status_claa, email, password) values (%s,"
        " %s, %s, %s)")

    hashed_password = hash_password(password)

    data = (name, status_claa, email, hashed_password)
    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


def group_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from claa.groups where email = %s")
    cursor.execute(query, (email, ))
    group_exists = cursor.fetchone()

    cursor.close()
    cnx.close()

    if group_exists is None:
        return False
    else:
        return True


def insert_group(name, email, insta, page, nof_scholarships, nof_volunteers,
                 address, campus, center):
    # todo fix
    email_tutor = "1@1"  # it should exists in tutors table

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "insert into claa.groups "
        "(name, email, instagram, webpage, nof_scholarships, nof_volunteers,"
        " address, campus, center, email_tutor) "
        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    data = (name, email, insta, page, nof_scholarships,
            nof_volunteers, address, campus, center, email_tutor)

    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


report = {}


def update_report(**kwargs):
    report[[*kwargs.keys()][0]] = [*kwargs.values()][0]


def insert_report():
    global report

    # todo fix
    group_email = "1@1"  # it should exists in groups table

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    print(report)

    query = (
        "INSERT INTO reports (activities_articulation, politics_articulation, "
        "selection_students, permanence_students, ufsc_target_public, "
        "society_target_public, infrastructure_condition,"
        "infrastructure_description, tools_condition, tools_description, "
        "costing_condition, costing_description, year, group_email) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    year = datetime.now().year

    data = (
        report['activities_articulation'],
        report['politics_articulation'],
        report['selection_students'],
        report['permanence_students'],
        report['ufsc_target_public'],
        report['society_target_public'],
        report['infrastructure_condition'],
        report['infrastructure_description'],
        report['tools_condition'],
        report['tools_description'],
        report['costing_condition'],
        report['costing_description'],
        year,
        group_email
    )

    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()

    report = {}
