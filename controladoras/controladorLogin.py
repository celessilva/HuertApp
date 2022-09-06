from app import app
from flask import g
from flask import session, flash,render_template,request,redirect,url_for
from model.consultasPublicacion import get_all_publicaciones
from model.forms import LoginForm

@app.route('/')
def index():
    title = "Home"
    username = ""
    banner = ""
    publicaciones = get_all_publicaciones()

    if len(publicaciones) == 0:
        error = "No existen publicaciones"
        app.logger.warn(error)
        flash(error)

    if 'username' in session:
        username = session['username']
        flash("Bienvenido: "+username)
    else:
        app.logger.warn("no LOGEADO") #AL LOG
        banner = "Bienvenido: te invitamos a logearte o registrarte en nuestra app "
    return render_template('index.html', username = g.username, title=title, banner=banner,publicaciones = publicaciones)

@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    desc_form = LoginForm()
    if request.method == 'POST' and desc_form.validate() :
        username = desc_form.username.data
        password = desc_form.password.data
        # COMPROBAR QUE EL USUARIO EXISTA EN LA DB
        if username :
            session['username'] = username
            return redirect(url_for("index"))
        else:
            flash("Los datos no pertenecen a un usuario registrado..")
    return render_template('login.html',title=title, form=desc_form)

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for("index"))