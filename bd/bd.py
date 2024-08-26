import mysql.connector

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
    query_data = (email, password)
    cursor.execute(query, query_data)

    # retorna apenas um registro ou None
    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    if type(result) == type(None):
        return False
    else:
        return result


def register_tutor(name, status_claa, email, password):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    query = ("select 1 from usuarios where email = %s")
    cursor.execute(query, (email, ))
    email_exists = cursor.fetchone()

    if email_exists is None:
        # todo: alerts users

    print("email exists:", email_exists)

    cursor.close()
    cnx.close()


def signup():
    pass


def set_user():
    pass


def get_group_pet():
    pass


def get_email():
    pass

    # cnx = mysql.connector.connect(**config)
    # cursor = cnx.cursor()

    # add_usuario = ("insert into usuarios"
    #                "(nome, membro_claa, email)"
    #                "values (%s, %s, %s)")
    # data_usuario = ('joao', 'nao', 'santosjoao301@gmail.com')

    # cursor.execute(add_usuario, data_usuario)
    # cnx.commit()

    # cursor.close()
    # cnx.close()
