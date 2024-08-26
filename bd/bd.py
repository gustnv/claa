import mysql.connector

config = {
  'user': 'root',
  'password': '2001',
  'host': '127.0.0.1',
  'database': 'claa',
  'raise_on_warnings': True
}

# retorna false se não tem usuario
def get_user(email, password):
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


def set_user():
    pass

def get_group_pet():
    pass

def signup():
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