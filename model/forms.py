from wtforms import StringField,validators
from wtforms.fields.simple import SubmitField, TextAreaField
from flask_wtf import FlaskForm
from app import mysql

# CUSTOM VALIDATIONS
# ES EL LUGAR PARA CHEQUEAR SI LOS DATOS SON CORRESPONDIDOS EN LA DB? ??
def validate_excluded_chars(self,field):
    excluded_chars = " *?!'^+%&/()=}][{$#"
    for char in self.username.data:
        if char in excluded_chars:
            raise validators.ValidationError(
                f"No se permiten los siguientes caracteres: {excluded_chars}")

def verificate_duplicated_username(self,field):
    username= self.username.data
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM usuarios where username = %s",[username,])
    usuario = cur.fetchall()[0]
    if usuario:
        raise validators.ValidationError("el usuario ya existe")

def verificate_username_exist_create(self):
     username= self.username.data
     cur = mysql.connection.cursor()
     cur.execute("SELECT username FROM usuarios where username = %s",[username,])
     usuario = cur.fetchall()[0]
     if usuario:
         raise validators.ValidationError("el usuario ya existe")

def verificate_username_exist(email,password):
     try:
         cur = mysql.connection.cursor()
         cur.execute('SELECT * FROM usuarios WHERE email = %s AND password = %s', (email, password,))
         # DEVUELVE UNA TUPLA, con un unico valor.
         account = cur.fetchone()
         return account
     except IndexError:
         validators.ValidationError("El usuario no existe")
     finally:
         cur.close()
         
def create_user_database(nombre,email,password):
    try:
         cur = mysql.connection.cursor()
         cur.execute('INSERT INTO usuarios(nombre, email, password) VALUES (%s,%s,%s)', (nombre,email,password))
         mysql.connection.commit()
    except IndexError:
         validators.ValidationError("El usuario no existe")
    finally:
         cur.close()
# -------------------

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.DataRequired(message="Username es requerido")
        ]) 
    apellido = StringField('Apellido',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.DataRequired(message="Username es requerido")
        ]) 
    direccion = StringField('Direccion',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.DataRequired(message="Username es requerido")
        ]) 
    username = StringField('Username',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.DataRequired(message="Username es requerido"),
        ]) 
    password = StringField('Password',[
        validators.length(max=255,message="El tamaño maximo es 255"),
        validators.DataRequired(message="Password Requerido")
    ])



class PublicacionForm(FlaskForm):
    titulo = StringField('Titulo',[
        validators.length(min=10,max=35,message="Ingrese Titulo valido. Entre 10 y 25 caracteres."),
        validators.DataRequired(message="Titulo es requerido")
        ]) 
    descripcion = TextAreaField('Descripcion',[
        validators.length(min=10, max=255,message="Ingrese un comentario valido. Entre 10 y 255 caracteres."),
        validators.DataRequired(message="La descripcion es requerida.")
    ])

class LoginForm(FlaskForm):
    username = StringField('Username',[
        validators.length(min=5,max=25,message="Ingrese usuario valido. Entre 5 y 25 caracteres."),
        validators.DataRequired(message="Username es requerido"),
        validate_excluded_chars
        ]) 
    password = StringField('Password',[
        validators.length(min=5,max=25,message="Debe ser mayor a 5 caracteres."),
        validators.DataRequired(message="Password es requerido")
        ]) 
    submit = SubmitField('Login')
                