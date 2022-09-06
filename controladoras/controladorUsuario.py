from app import app
from flask import request,flash,render_template,make_response
from model.forms import UsuarioForm

# 
@app.route('/create_user/',methods=['GET','POST'])
def create_user():
    title = "Alta Usuarios"
    form = UsuarioForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        # CREA USUARIO, FALTA IMPLEMENTAR
        flash(f"Usuario: {username} creado")
    
    return render_template('create_user.html', title=title, form=form )







