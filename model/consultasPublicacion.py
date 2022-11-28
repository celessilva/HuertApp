from app import *
from flask import flash
from flask_mysqldb import MySQL, MySQLdb
from werkzeug.utils import redirect
from flask.helpers import url_for

def crearPublicacion(titulo:str,descripcion:str,id_usuario:int,foto:str) -> bool:
    response = False
    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO Publicacion (titulo, descripcion,id_usuario,foto) VALUES (%s,%s,%s,%s)", (titulo,descripcion,id_usuario,foto))
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
        cur.execute(f"SELECT * from Usuario where nombre = '{username}';")
        resultado =cur.fetchall()[0]
        #DEVUELVE UNA TUPLA
    except IndexError:
        app.logger.error(IndexError)
    finally:
        cur.close()
    return resultado

def get_usuario_by_email(email:str) -> tuple:
    resultado = ()
    try:
        cur = mysql.connection.cursor()
        # TODO : INSEGURO? PORQUE?... 
        cur.execute(f"SELECT * from Usuario where email = '{email}';")
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
        cur.execute(f"SELECT * from Publicacion INNER JOIN  Usuario ON Publicacion.id_usuario = Usuario.id_usuario WHERE id_publicacion = {id};")
        resultado = cur.fetchone()
    except IndexError:
        app.logger.error(IndexError)
        resultado = (False)
    finally:
        cur.close()
    return resultado

def get_all_publicaciones(numero_pagina)-> tuple:
    data= [] 
    cur = mysql.connection.cursor()
    try:
        cur.execute(f"SELECT * from Publicacion ORDER BY id_publicacion DESC LIMIT 3 OFFSET {numero_pagina} ;")
        data = cur.fetchall()
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        app.logger.error(e)
    finally:
        cur.close()
    return data

def get_all_publicaciones_paginacion()-> tuple:
    data= [] 
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM Publicacion")
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
        cur.execute(f"SELECT * from Publicacion where id_usuario = '{username}';")
        data = cur.fetchall()
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
            cur.execute(f"DELETE from Publicacion where id_publicacion = {id};")
            mysql.connection.commit()
            resultado = True 
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            resultado = False
            app.logger.error(MySQLdb.Error)
            app.logger.error("No se pudo borrar")
        finally:
            cur.close()
    return resultado

def update_publicacion(titulo,descripcion,foto,id)->str:
    resultado = False
    try:
        cur = mysql.connection.cursor()
        #ESTA ES LA FORMA DE AGREGAR DATOS.
        cur.execute("""
        UPDATE Publicacion
        SET titulo=%s,
            descripcion=%s, 
            foto=%s
        WHERE id_publicacion = %s""",(titulo,descripcion,foto,id))
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
        cur.execute(f"SELECT id_usuario from Publicacion where id_publicacion = '{id_publicacion}';")
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


