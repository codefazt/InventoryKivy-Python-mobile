import hashlib, binascii, os
import sqlite3
from sqlite3 import Error

class Sqlconexion():
    

    def create_DataBase(self):
        
        try:
            path = os.getcwd()
            con = sqlite3.connect(path + '/InventarioDB.db')
            return con

        except Error:
            print('Error al Crear Conexion', Error)

    
    def create_Table(self,con):
 
        cursorObj = con.cursor()
        #Tabla de Usuarios
        cursorObj.execute("CREATE TABLE if not exists User(id integer PRIMARY KEY, cedula text, nombre text, cargo integer, clave text, fecha text)")
        con.commit()
        
        #tablas de Productos
        
        #supTabla Principal
        cursorObj.execute("CREATE TABLE if not exists productos(id integer PRIMARY KEY, nombre text, categoria integer)")
        con.commit()
        
        #preTabla lista de categorias tanto para Productos como para Usuarios etc.
        cursorObj.execute("CREATE TABLE if not exists categorias(id integer PRIMARY KEY, codigo text, nombre text, categoria integer, img text)")
        con.commit()
        
        #supTabla detellas productos
        cursorObj.execute("CREATE TABLE if not exists detelles_productos(id integer PRIMARY KEY, codigo text, nombre text, categoria integer, cantidad text, precio text, peso text, foto text)")
        con.commit()
    
    def sql_insert(self, con, User):
        
        User[3] = hash_password(User[3])

        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO User(cedula, nombre, cargo, clave, fecha) VALUES(?, ?, ?, ?, ?)', User)      
        con.commit()

    def sql_insert_producto(self, con, producto):
        
        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO productos(nombre, categoria) VALUES(?, ?)', producto)      
        con.commit()

    def sql_insert_categoria(self, con, categoria):
        
        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO categorias(nombre, categoria, img) VALUES(?, ?, ?)', categoria)      
        con.commit()

    def sql_insert_detelles_productos(self, con, producto):
        
        cursorObj = con.cursor()
        cursorObj.execute('INSERT INTO detelles_productos(codigo, nombre, categoria, cantidad, precio, peso, foto) VALUES(?,?,?,?,?,?,?)', producto)      
        con.commit()

    def sql_fetch(self, tabla, con):
 
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM {0}'.format(tabla))
        rows = cursorObj.fetchall()
        
            
        return rows

    def sql_fetch_with_param(self, tabla, con, parametro, dato_param):
 
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM {0} WHERE {1} = {2}'.format(tabla, parametro, dato_param))
        rows = cursorObj.fetchall()
        
            
        return rows

    def fetch_one(self, con, table, campo, condicion):

        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM {0} WHERE {1} = "{2}" '.format(table, campo, condicion))
        return cursorObj.fetchall()
    
    def fetch_one_with_query(self, con, query):

        cursorObj = con.cursor()
        cursorObj.execute(query)
        return cursorObj.fetchall()

    def close_db(self, con):
        con.close()



# Funcion para Encriptar y desenccriptar
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password