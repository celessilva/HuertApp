from app import app
from flask import g
from flask import session, flash,render_template,request,redirect,url_for
from model.consultasPublicacion import get_all_publicaciones, get_all_publicaciones_paginacion
from model.forms import LoginForm, verificate_username_exist

@app.route('/')
def inicio():
    return redirect(url_for('index', numero_pagina=1))

@app.route('/<int:numero_pagina>')
def index(numero_pagina):
    title = "Home"
    banner = ""

    #Obtiene todas las publicaciones segun la paginación dada
    if numero_pagina == 1:
        publicaciones = get_all_publicaciones(0)
    else:
        publicaciones = get_all_publicaciones((numero_pagina*3)-3)

    #Obtiene toda las publicaciones pasa saber cuanta paginación llevara el home
    publicaciones_paginacion = get_all_publicaciones_paginacion()

    #Para la paginacion manual...
    paginaciones = 1
    contador = 0

   
    for item in range(len(publicaciones_paginacion)):
        if contador > 2:
            paginaciones = paginaciones +  1
            contador = 0
        contador = contador +1 
        
    
    if len(publicaciones) == 0:
        error = "No existen publicaciones"
        app.logger.warn(error)
        paginaciones = 0
        flash(error)

    if 'username' not in session:
        banner = "Bienvenido: te invitamos a loguearte o registrarte en nuestra app "
    return render_template('index.html', username = g.username, title=title, banner=banner,publicaciones = publicaciones, paginaciones=paginaciones+1, len=len)

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
            if account[6] == None:
                session['celular'] = "No se encontro numero de celular"
            else:
                session['celular'] = account[6]
            if 'username' in session:
                username = session['username']
                flash("Bienvenido: "+username)
            return redirect(url_for("index", numero_pagina=1))
    return render_template('login.html',title=title, form=desc_form)

# ------------------------------------------------------------------------------------------

#Ruta para el logout (elimina las "keys" guardadas en session)
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    if 'id_usuario' in session:
        session.pop('id_usuario')     
    return redirect(url_for("index",numero_pagina=1))

