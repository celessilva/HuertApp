from flask import Flask
from flask.templating import render_template
from flask import g
from flask_wtf import CSRFProtect
from flask_mysqldb import MySQL
from flask import session

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'

#Comento esto porque hay una libreria que trae un diccionario con todos los tipos de imagen permitidos y estan siendo validados a traves de Flask-WTF
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.errorhandler(404)
def page_not_found(e):
    title = "404"
    msg = "Page not found."
    return render_template('404.html', title=title, msg=msg), 404

app.config.from_object('config.DevelopmentConfig')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_error_handler(404, page_not_found)

mysql = MySQL(app)
csrf = CSRFProtect(app)

from controladoras.controladorLogin import *
from controladoras.controladorPublicaciones import *
from controladoras.controladorUsuario import *

@app.before_request
def before_request():
    # chequeo de datos de session/DBs
    # GLOBAL malapractica?
    g.username = ""
    if 'username' in session:
        g.username =  session['username']
    


if __name__ == '__main__':
    csrf.init_app(app)
    app.run(port = 3000)
