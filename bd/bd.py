import mysql.connector
import bcrypt

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

    query = "select senha from usuarios where email = %s"
    cursor.execute(query, (email, ))

    result = cursor.fetchone()
    cursor.close()
    cnx.close()

    if result is None:
        return False

    stored_password = result[0]
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        return True
    else:
        return False


def tutor_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from usuarios where email = %s")
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
        "insert into usuarios (nome, membro_claa, email, senha) values (%s, %s, %s, %s)")

    if status_claa == "Não.":
        status_claa = "nao"
    elif status_claa == "Sim, Titular.":
        status_claa = "titular"
    elif status_claa == "Sim, Suplente.":
        status_claa = "suplente"

    hashed_password = hash_password(password)

    data = (name, status_claa, email, hashed_password)
    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


def group_exists(email):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from grupos_pet where email = %s")
    cursor.execute(query, (email, ))
    group_exists = cursor.fetchone()

    cursor.close()
    cnx.close()

    if group_exists is None:
        return False
    else:
        return True


def insert_group(name, email, insta, page, nof_scholarships, nof_volunteers, address, campus, center):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = (
        "INSERT INTO grupos_pet "
        "(nome, email, instagram, pagina, nof_bolsistas, nof_voluntarios, endereco, campus, centro) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )

    data = (name, email, insta, page, nof_scholarships,
            nof_volunteers, address, campus, center)

    cursor.execute(query, data)
    cnx.commit()

    cursor.close()
    cnx.close()


def set_user():
    pass


def get_group_pet():
    pass
