from app import app
from flask import request,flash,render_template,make_response
from model.forms import UsuarioForm, verificate_username_exist, verificate_username_exist_create
from model.forms import create_user_database
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
        if verificate_username_exist_create(email):
            flash(f"Otro usuario con email {email} ya existe")
        else:
            create_user_database(nombre,email,password)
            flash(f"Usuario: {nombre} creado")
    return render_template('create_user.html', title=title, form=form )






