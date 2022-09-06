from app import *
from flask import flash
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.utils import redirect
from flask.helpers import url_for

def crearPublicacion(titulo:str,descripcion:str,usuario:str) -> bool:
    response = False
    cur = None
    try:
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO publicaciones (titulo, descripcion,usuario) 
        VALUES (%(titulo)s,%(descripcion)s,%(usuario)s)""",
        {'titulo':titulo,'descripcion':descripcion,'usuario':usuario})
        mysql.connection.commit()
        response = True 
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        app.logger.error(e)
    finally:
        cur.close()
    return response

def get_usuario_by_username(username:str) -> tuple:
    resultado = ()
    try:
        cur = mysql.connection.cursor()
        # TODO : INSEGURO? PORQUE?... 
        cur.execute(f"SELECT * from usuarios where username = {username};")
        resultado =cur.fetchall()[0]
        #DEVUELVE UNA TUPLA
    except IndexError:
        app.logger.error(IndexError)
    finally:
        cur.close()
    return resultado


def get_publicacion_by_id(id:int) -> tuple:
    resultado = None
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from publicaciones where id = {id};")
        resultado =cur.fetchall()[0]
        print(resultado)
    except IndexError:
        app.logger.error(IndexError)
        resultado = (False)
    finally:
        cur.close()
    return resultado

def get_all_publicaciones()-> tuple:
    data= [] 
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM publicaciones")
        data = cur.fetchall()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        app.logger.error(e)
    finally:
        cur.close()
    return data

def get_all_publicaciones_by_username(username)-> tuple:
    data= [] 
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT * from publicaciones where usuario = '{username}';")
        data = cur.fetchall()
        print(data)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        app.logger.error(e)
    finally:
        cur.close()
    return data

def delete_publicacion_by_id(id:int)->bool:
    resultado = None
    publicacion= get_publicacion_by_id(id)
    if publicacion == False:
       resultado = False 
    else:
        try:
            cur = mysql.connection.cursor()
            cur.execute(f"DELETE from publicaciones where id = {id};")
            mysql.connection.commit()
            resultado = True 
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            resultado = False
            app.logger.error(MySQLdb.Error)
            app.logger.error("No se pudo borrar")
        finally:
            cur.close()
    return resultado

def update_publicacion(titulo,descripcion,id)->str:
    resultado = False
    try:
        cur = mysql.connection.cursor()
        #ESTA ES LA FORMA DE AGREGAR DATOS.
        cur.execute("""
        UPDATE publicaciones 
        SET titulo=%s,
            descripcion=%s 
        WHERE id = %s""",(titulo,descripcion,id))
        mysql.connection.commit()
        app.logger.warn("UPDATEADO")
        resultado = True 
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        app.logger.error(e)
    finally:
        cur.close()
    return resultado

def publicacion_belongs_usuario(id_publicacion,username)->bool:
    resultado = False
    try:
        cur = mysql.connection.cursor()
        #Devuelve el usuario de la publicacion
        cur.execute(f"SELECT usuario from publicaciones where id = '{id_publicacion}';")
        data = cur.fetchall()[0]
        # RECORDAR DEVUELVE UNA TUPLA!!
        app.logger.warn(data)
        if data[0] == username:
            resultado = True 
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        app.logger.error(e)
    finally:
        cur.close()

    return resultado


