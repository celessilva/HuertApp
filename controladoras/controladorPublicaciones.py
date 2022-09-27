from flask import g
from app import app
from model.forms import PublicacionForm
from flask import session, flash,render_template,request,redirect,url_for
import model.consultasPublicacion as consultasPublicacion 

#CREA PUBLICACIONES
# VERONICA
@app.route('/crear_publicacion', methods=['GET', 'POST'])
def crear_publicacion():
    title = "Crear Publicacion"
    desc_form = PublicacionForm(request.form)
    titulo = desc_form.titulo.data
    descripcion = desc_form.descripcion.data

    if request.method == 'POST' and desc_form.validate() and 'username' in session:
        username = session['id_usuario']
        # usuario = consultasPublicacion.get_usuario_by_username(username)
        if (consultasPublicacion.crearPublicacion(titulo,descripcion,username)==True):
            flash(f"Publicacion:{desc_form.titulo.data}, creada con exito.")
        else:
            flash(f"Error al crear publicacion. Intentelo de nuevo en unos minutos.")


    return render_template('create_publicacion.html', title=title, form=desc_form, username = g.username )

#LISTA DE TODAS LAS PUBLICACIONES
# naivis
@app.route('/mis_publicaciones', methods=['GET'])
def mis_publicaciones():
    error = ""
    msgError = ""
    banner = "Mis Publicaciones"
    username = session['id_usuario']
    # MODELO
    data = consultasPublicacion.get_all_publicaciones_by_username(username)
    if len(data) == 0:
        error = "Lista Vacia"
        msgError = "No existen publicaciones del usuario."
    # VISTAS
    return render_template('mis_publicaciones.html',banner = banner, error=error, msgError=msgError, publicaciones=data,username = username)

# nico
@app.route('/publicacion/<int:id>/',methods=['GET'])
def get_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    if publicacion == False:
        flash("No existe la publicacion")
        return redirect(url_for("mis_publicaciones"))
        
    return render_template('publicacion.html', publicacion = publicacion,username = g.username )
# nic


# La pagina donde se edita, completa el form con los datos de la publicacion 
@app.route('/edit/<int:id>/', methods=['GET', 'POST'])
def edit_publicacion(id):
    title="EDITAR"
    username = session['id_usuario']
    # Comprobar que existe la publicacion
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    form = PublicacionForm()

    if existe_publicacion(publicacion) and consultasPublicacion.publicacion_belongs_usuario(id,username):
        # Pasa informacion al form
        """Paso la tupla que devuelve la busqueda de publicacion a cada uno de los campos del form"""
        form.titulo.data = publicacion[1]
        form.descripcion.data = publicacion[2]
    else:
        # NO es necesario darle toda la informacion al "usuario".
        return redirect(url_for("index"))

    return render_template('edit-publicacion.html',form = form,title=title, publicacion=publicacion, username = username)

# Realiza el update 
@app.route('/update/<int:id>/',methods=['POST'])
def update_publicacion(id):
    publicacion = consultasPublicacion.get_publicacion_by_id(id)
    form = PublicacionForm()
    if publicacion and request.method == 'POST' and form.validate():
        titulo = form.titulo.data
        descripcion = form.descripcion.data
        # Comprobar que la publicacion se actualizo satisfactoriamente.
        if consultasPublicacion.update_publicacion(titulo,descripcion,id):
            flash("Publicación actualizada exitosamente")
            return redirect(url_for("mis_publicaciones"))
        else:
            flash("No se pudo actualizar correctamente. Intentelo de nuevo mas tarde.")

    
    return render_template('edit-publicacion.html',form = form, publicacion = publicacion, username = g.username)

def existe_publicacion(publicacion) -> bool:
    resultado = None
    if not publicacion :
        # TODO:
        # Flash permite ponerle categorias a los mensajes. 
        # Implementar luego.
        flash("No existe la publicacion.","error")
        resultado = False
    else:
        resultado = True
    return resultado

@app.route('/delete/<int:id>/', methods=['GET', 'POST'])
def delete_publicacion(id):
    publicacion = consultasPublicacion.delete_publicacion_by_id(id)
    app.logger.warn("borrando la publicacion")
    if publicacion == False:
        flash("No se pudo borrar la publicacion")
        return redirect(url_for("index"))
    else:
        flash("Publicación borrada exitosamente")
        return redirect(url_for("mis_publicaciones"))