from app import app
from flask import g
from flask import request,flash,render_template,make_response
from model.forms import UsuarioForm
from model.forms import create_user_database

# 
@app.route('/create_user/',methods=['GET','POST'])
def create_user():
    title = "Alta Usuarios"
    form = UsuarioForm(request.form)
    if request.method == 'POST':
        apellido = form.apellido.data
        nombre = form.nombre.data
        email = form.username.data
        password = form.password.data
        create_user_database(nombre,email,password)

        flash(f"Usuario: {nombre} creado")
    
    return render_template('create_user.html', title=title, form=form )







