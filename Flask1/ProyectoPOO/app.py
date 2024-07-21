from flask import Flask, request,render_template
from flask_mysqldb import MySQL


app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='bdflask'
mysql= MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardarNombre', methods=['POST'])
def guardarNombre():
   if request.method=='POST':
       titulo= request.form['txtTitulo']
       artista= request.form['txtArtista']
       anio= request.form['txtAnio']
       print(titulo, artista, anio)
       return 'Datos recibidos en el server'


#Manejador de exepciones 
@app.errorhandler(404)
def paginano(e):
    return'Revisa tu sintaxis, no encontre nada'

if __name__=='__main__':
    app.run(port=3000, debug=True)












    from flask import Flask, request,render_template,url_for,redirect,flash
from flask_mysqldb import MySQL


app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='albums'
mysql= MySQL(app)

app.secret_key='mysecretkey'