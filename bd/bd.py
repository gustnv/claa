import mysql.connector

config = {
  'user': 'root',
  'password': '2001',
  'host': '127.0.0.1',
  'database': 'claa',
  'raise_on_warnings': True
}

def have_user(email, password):
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