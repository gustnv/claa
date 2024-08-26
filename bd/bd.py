import mysql.connector
import time

config = {
    'user': 'root',
    'password': 'P4ssw0rd!',
    'host': '127.0.0.1',
    'database': 'claa',
    'raise_on_warnings': True
}


def login(email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select * from usuarios where email = %s and senha = %s")

    hashed_password = hash(password)
    data = (email, hashed_password)

    cursor.execute(query, data)

    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    if result is None:
        return False
    else:
        return result


def email_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from usuarios where email = %s")
    cursor.execute(query, (email, ))
    email_exists = cursor.fetchone()

    cursor.close()
    cnx.close()

    if email_exists is None:
        return False
    else:
        return True


def insert_tutor(name, status_claa, email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "insert into usuarios (nome, status_claa, email, senha) values (%s, %s, %s, %s)")

    if status_claa == "Não.":
        status_claa = "nao"
    elif status_claa == "Sim, Titular.":
        status_claa = "titular"
    elif status_claa == "Sim, Suplente.":
        status_claa = "suplente"

    hashed_password = hash(password)

    data = (name, status_claa, email, hashed_password)
    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


def signup():
    pass


def set_user():
    pass


def get_group_pet():
    pass
