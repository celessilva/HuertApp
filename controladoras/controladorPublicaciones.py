from ast import For
from concurrent.futures import thread

from queue import Empty
from flask import g
from app import app
from model.forms import PublicacionForm, PublicacionEditForm
from flask import session, flash, render_template, request, redirect, url_for
import model.consultasPublicacion as consultasPublicacion
from controladoras import controladorUsuario
from werkzeug.utils import secure_filename
import os
from werkzeug.datastructures import CombinedMultiDict

# CREA PUBLICACIONES -------------------------------------------------------
# VERONICA
@app.route('/crear_publicacion', methods=['GET', 'POST'])
def crear_publicacion():
    title = "Crear Publicacion"
    #Diccionario que combina los archivos que recibe el request y los string que vienen del POST
    desc_form = PublicacionForm(CombinedMultiDict((request.files, request.form)))
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data
    #Recibe Foto
    foto = desc_form.foto.data
    
    if request.method == 'POST' and desc_form.validate() and 'username' in session:
        username = session['id_usuario']
        filename = secure_filename(foto.filename)

        #Ruta donde se guardan las fotos de las publicaciones
        path = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],filename)
        #Guarda la foto en la ruta generada arriba...
        foto.save(path)
        
        # usuario = consultasPublicacion.get_usuario_by_username(username)
        if (consultasPublicacion.crearPublicacion(titulo, descripcion, username,filename) == True):
            flash(f"Publicacion:{desc_form.titulo.data}, creada con exito.")

        else:
            flash(f"Error al crear publicacion. Intentelo de nuevo en unos minutos.")
    return render_template('create_publicacion.html', title=title, form=desc_form, username=session['username'])
    

# LISTA DE TODAS LAS PUBLICACIONES -------------------------------------------------------
# naivis
@app.route('/mis_publicaciones', methods=['GET'])
def mis_publicaciones():
    error = ""
    msgError = ""
    banner = "Mis Publicaciones"
    data = None
    username = None
    # Check para ver si la clave se encuentra en la session
    if 'id_usuario' in session:
        username = session['id_usuario']
        data = consultasPublicacion.get_all_publicaciones_by_username(username)
    # En caso de no encontrarse y dirijirse a la ruta procede a mostrar un mensaje pidiendo acceso al sistema
    
    elif 'id_usuario' not in session:
        error = "Usuario no logueado"
        msgError = "Usted debe loguearse al sistema para poder crear o ver sus publicaciones"
    # Si los datos traidos no contienen nada
    if data != None:
        if len(data) == 0:
            error = "Lista Vacia"
            msgError = "No existen publicaciones del usuario."
    # VISTAS
    return render_template('mis_publicaciones.html', banner=banner, error=error, msgError=msgError, publicaciones=data, username=username)

# nico
# Ruta para mostrar la publicacion seleccionada por "id" -------------------------------------------------------
@app.route('/publicacion/<int:id>/', methods=['GET'])
def get_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    datos_usuario = consultasPublicacion.get_usuario_by_email(publicacion[8])
    if publicacion == False:
        flash("No existe la publicacion")
        return redirect(url_for("mis_publicaciones"))
    return render_template('publicacion.html', publicacion=publicacion, username=publicacion[7], user=datos_usuario)
# nic


# La pagina donde se edita, completa el form con los datos de la publicacion -------------------------------------------------------
@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    title = "EDITAR"
    username = session['id_usuario']
    # Comprobar que existe la publicacion
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    form = PublicacionForm()

    if existe_publicacion(publicacion) and consultasPublicacion.publicacion_belongs_usuario(id, username):
        # Pasa informacion al form
        """Paso la tupla que devuelve la busqueda de publicacion a cada uno de los campos del form"""
        form.titulo.data = publicacion[1]
        form.descripcion.data = publicacion[2]
        form.foto.data = publicacion[5]
    else:
        # NO es necesario darle toda la informacion al "usuario".
        return redirect(url_for("index",numero_pagina=1))
    return render_template('edit-publicacion.html', form=form, title=title, publicacion=publicacion, username=username)

# Realiza el update a la publicacion seleccionada -------------------------------------------------------
@app.route('/update/<int:id>/', methods=['POST'])
def update_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    form = PublicacionEditForm(CombinedMultiDict((request.files, request.form)))
    if publicacion and request.method == 'POST' and form.validate():
        titulo = form.titulo.data
        descripcion = form.descripcion.data

        #Foto que viene del formulario para editar
        foto = form.foto.data

        #Si la data que viene del formulario para el atributo foto NO ES "None" entonces borra la foto y sube la nueva, caso CONTRARIO no hace nada mas que actualizar
        #el nombre con el anterior, esto es para permitir al editar poder guardar la misma foto sin necesidad de seleccionarla nuevamente...
        if form.foto.data is not None:
            if publicacion[5]:
                try:
                    os.unlink(os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],publicacion[5]))
                except:
                    flash("No se encontro la imagen anterior...continuar...")
            filename = secure_filename(foto.filename)
            #Ruta para guardar...(se puede crear una funcion a parte en caso de ser necesario)
            path = os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],filename)
            foto.save(path)
        else:
            filename = publicacion[5]

        # Comprobar que la publicacion se actualizo satisfactoriamente.
        if consultasPublicacion.update_publicacion(titulo, descripcion,filename, id):
            flash("Publicación actualizada exitosamente")
            return redirect(url_for("mis_publicaciones"))
        else:
            flash("No se pudo actualizar correctamente. Intentelo de nuevo mas tarde.")
    return render_template('edit-publicacion.html', form=form, publicacion=publicacion, username=g.username)

#Verifica si existe la publicacion -------------------------------------------------------
def existe_publicacion(publicacion) -> bool:
    resultado = None
    if not publicacion:
        # TODO:
        # Flash permite ponerle categorias a los mensajes.
        # Implementar luego.
        flash("No existe la publicacion.", "error")
        resultado = False
    else:
        resultado = True
    return resultado

#Borra la publicacion seleccionada -------------------------------------------------------
@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    publicacion_foto = consultasPublicacion.get_publicacion_by_id(id)
    filename = publicacion_foto[5]
    publicacion = consultasPublicacion.delete_publicacion_by_id(id)

    try:
        #Elimina la foto solo si la encuentra para eso el "try" se puede implementar en donde sea necesario capturar el error...
        os.unlink(os.path.join(app.root_path,app.config['UPLOAD_FOLDER'],filename))
    except:
        flash("No se encontro la ruta o imagen.")

    app.logger.warn("borrando la publicacion")

    if publicacion == False:
        flash("No se pudo borrar la publicacion")
        return redirect(url_for("index",numero_pagina=1))
    else:
        flash("Publicación borrada exitosamente")
        return redirect(url_for("mis_publicaciones"))
    return filename
    