from app import app
from flask import request,flash,render_template,make_response,redirect,url_for, session
from model.forms import UsuarioForm, verificate_username_exist, verificate_username_exist_create, PerfilForm
from model.forms import create_user_database, update_usuario
from model.consultasPublicacion import get_usuario_by_username
from werkzeug.security import generate_password_hash

# Ruta para el registro de cuentas
@app.route('/create_user/',methods=['GET','POST'])
def create_user():
    title = "Crear Cuenta"
    form = UsuarioForm(request.form)
    
    if request.method == 'POST':
        nombre = form.nombre.data
        email = form.username.data   
        password = generate_password_hash(form.password.data) 
        celular = form.celular.data
        if verificate_username_exist_create(email):
            flash(f"Otro usuario con email {email} ya existe")
        else:
            create_user_database(nombre,email,password,celular)
            flash(f"Usuario: {nombre} creado")
            return redirect(url_for("index",numero_pagina=1))
    return render_template("create_user.html", title=title, form=form )


@app.route('/perfil/',methods=['GET','POST'])
def perfil():
    form = PerfilForm(request.form)
    usuario = get_usuario_by_username(session['username'])
    title= 'Editar Perfil'
    if request.method == 'POST' and form.validate():
        update_usuario(form.nombre.data,form.celular.data,usuario[0])
        session['username'] = form.nombre.data
        session['celular'] = form.celular.data
        return redirect(url_for('index', numero_pagina=1))
    if session['username'] and usuario:
        form.nombre.data = session['username']
        if session['celular'] == None:
            form.celular.data = "No se encontro un celular"
        else:
            form.celular.data = session['celular']
    return render_template('perfil.html',title = title, form=form)






