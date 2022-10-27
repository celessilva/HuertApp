from tokenize import String
from typing import Tuple
from wtforms import StringField,validators
from wtforms.fields.simple import SubmitField, TextAreaField, EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired, ValidationError
from flask_wtf import FlaskForm
from flask import flash
from app import mysql
from werkzeug.security import check_password_hash
from wtforms.widgets import PasswordInput
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from flask_uploads import UploadSet, IMAGES


# CUSTOM VALIDATIONS
# ES EL LUGAR PARA CHEQUEAR SI LOS DATOS SON CORRESPONDIDOS EN LA DB? ??
def validate_excluded_chars(self,field):
    excluded_chars = " *?!'^+%&/()=}][{$#"
    for char in self.username.data:
        if char in excluded_chars:
            raise validators.ValidationError(
                f"No se permiten los siguientes caracteres: {excluded_chars}")

# ------------------------------------------------------------------------------------------

def verificate_duplicated_username(self,field):
    username= self.username.data
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM usuarios where username = %s",[username,])
    usuario = cur.fetchall()[0]
    if usuario:
        raise validators.ValidationError("el usuario ya existe")

# ------------------------------------------------------------------------------------------

def verificate_username_exist_create(username):

     cur = mysql.connection.cursor()
     cur.execute("SELECT email FROM Usuario where email = %s",[username])
     usuario = cur.fetchall()
     return True if usuario else False

# ------------------------------------------------------------------------------------------

#Verifica si el usuario existe en la base de datos (se usa para el login)
def verificate_username_exist(email:str,password:str)->Tuple:
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM Usuario WHERE email = %s", [email,])
        account = cur.fetchone()
        #Valida si encontro algun usuario en la base de datos con lo que viene del formulario
        if account == None:
            flash('Email o usuario no encontrado')
        #Si encontro algun usuario procede a checkear si la contraseña hasheada es la correcta
        else:
            pass_hash = account[3]
            #Verifica si lo que proviene del input password es el hash correcto en la base de datos
            if check_password_hash(pass_hash,password):
                #Si todo sale bien devuelve la cuenta en una tupla para crear la session
                return account
            else:
                flash('Contraseña Incorrecta')    
    except IndexError:
        validators.ValidationError("El usuario no existe")
    finally:
        cur.close()

# ----------------------------------------------------------------------------
         
#Crea el usuario en la base de datos
def create_user_database(nombre:str,email:str,password:str)-> None:
    try:
         cur = mysql.connection.cursor()
         cur.execute('INSERT INTO Usuario(nombre, email, password) VALUES (%s,%s,%s)', (nombre,email,password))
         mysql.connection.commit()
    except IndexError:
         validators.ValidationError("El usuario no existe")
    finally:
         cur.close()

# -------------------- VALIDACIONES DEL FORMULARIO --------------------------------------------

class UsuarioForm(FlaskForm):
    nombre = StringField('Nombre',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.DataRequired(message="Username es requerido")
        ]) 
    username = EmailField('Email',[
        validators.length(min=5,max=25,message="Ingrese Titulo valido"),
        validators.DataRequired(message="Username es requerido"),
        ]) 
    password = StringField('Contraseña',[
        validators.length(min=5,max=255,message="El tamaño maximo es 255"),
        validators.DataRequired(message="Password Requerido")
    ],
    widget=PasswordInput(hide_value=False))

def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024

    def file_length_check(form, field):
        if field.data is not None:
            if len(field.data.read()) > max_bytes:
                raise ValidationError(
                    f'Tamaño de archivo excedido. Tamaño maximo: {max_size_in_mb} MB')
            field.data.seek(0)
    return file_length_check

class PublicacionForm(FlaskForm):
    titulo = StringField('Titulo',[
        validators.length(min=10,max=35,message="Ingrese Titulo valido. Entre 10 y 25 caracteres."),
        validators.DataRequired(message="Titulo es requerido.")
        ]) 
    descripcion = TextAreaField('Descripcion',[
        validators.length(min=10, max=255,message="Ingrese un comentario valido. Entre 10 y 255 caracteres."),
        validators.DataRequired(message="La descripcion es requerida.")
    ])
    #VALIDADOR PARA LA FOTO
    foto = FileField('Seleccionar Foto',validators=[
        FileRequired(message="Necesitas subir una foto."),
        FileAllowed(IMAGES, "Solo imagenes porfavor!"),
        FileSizeLimit(0.5)
    ])

#Se creo una clase nueva para el editar puesto que si se agregan varios parametros innecesarios la validacion no deja continuar si faltan algunos de los campos
#en el formulario
class PublicacionEditForm(FlaskForm):
    titulo = StringField('Titulo',[
        validators.length(min=10,max=35,message="Ingrese Titulo valido. Entre 10 y 25 caracteres."),
        validators.DataRequired(message="Titulo es requerido.")
        ]) 
    descripcion = TextAreaField('Descripcion',[
        validators.length(min=10, max=255,message="Ingrese un comentario valido. Entre 10 y 255 caracteres."),
        validators.DataRequired(message="La descripcion es requerida.")
    ])
    #VALIDADOR PARA LA FOTO DEL EDIT (SIN REQUIRED)
    foto = FileField('Seleccionar Foto',validators=[
        FileAllowed(IMAGES, "Solo imagenes porfavor!"),
        FileSizeLimit(0.5)
    ])    
   


class LoginForm(FlaskForm):
    username = StringField('Email',[
        validators.length(min=5,max=25,message="Ingrese usuario valido. Entre 5 y 25 caracteres."),
        validators.DataRequired(message="Email es requerido"),
        validate_excluded_chars
        ]) 
    password = StringField('Password',[
        validators.length(min=5,max=25,message="Debe ser mayor a 5 caracteres."),
        validators.DataRequired(message="Password es requerido"),
        
        ],
        #Agregado para esconder el input del password durante el login
        widget=PasswordInput(hide_value=False)) 
    submit = SubmitField('Login')
                