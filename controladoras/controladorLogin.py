from app import app
from flask import g
from flask import session, flash,render_template,request,redirect,url_for
from model.consultasPublicacion import get_all_publicaciones
from model.forms import LoginForm, verificate_username_exist


@app.route('/')
def index():
    title = "Home"
    banner = ""
    publicaciones = get_all_publicaciones()
    #Devolver al reverso las publicaciones, de esta forma la mas nueva siempre esta primero...(proximo paso ¿fechas?)
    publicaciones = publicaciones[::-1]
   

    if len(publicaciones) == 0:
        error = "No existen publicaciones"
        app.logger.warn(error)
        flash(error)

    if 'username' not in session:
        banner = "Bienvenido: te invitamos a loguearte o registrarte en nuestra app "
    return render_template('index.html', username = g.username, title=title, banner=banner,publicaciones = publicaciones)

# ------------------------------------------------------------------------------------------

#Ruta para el login (verifica los datos que llegan del formulario con la base de datos asi como tambien el check correspondiente al hash del password)
@app.route('/login', methods=['GET', 'POST'])
def login():
    title = "Login"
    desc_form = LoginForm()
    if request.method == 'POST' and desc_form.validate() :
        username = desc_form.username.data
        password = desc_form.password.data
        
        # Comprueba los datos para validarlos con los que se encuentran en la base de datos
        account = verificate_username_exist(username,password)
        #Si el objeto devuelto contiene datos procede a crear la session y redirigir al index
        if account != None:
            session['username'] = account[1]
            session['id_usuario'] = account[0]
            if 'username' in session:
                username = session['username']
                flash("Bienvenido: "+username)
            return redirect(url_for("index"))
    return render_template('login.html',title=title, form=desc_form)

# ------------------------------------------------------------------------------------------

#Ruta para el logout (elimina las "keys" guardadas en session)
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    if 'id_usuario' in session:
        session.pop('id_usuario')     
    return redirect(url_for("index"))

