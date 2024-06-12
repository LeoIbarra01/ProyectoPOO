from flask import Flask, request,render_template,url_for,redirect,flash
from flask_mysqldb import MySQL


app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='albums'
mysql= MySQL(app)

app.secret_key='mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardarAlbum', methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        # Tomamos los datos que vienen por POST
        Ftitulo = request.form['txtTitulo']
        Fartista = request.form['txtArtista']
        Fanio = request.form['txtAnio']
        
        # Enviamos a la BD sin incluir la columna de clave primaria
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO albums(titulo, artista, anio) VALUES (%s, %s, %s)', (Ftitulo, Fartista, Fanio))
        mysql.connection.commit()
        flash('Álbum guardado correctamente')
        return redirect(url_for('index'))



#Manejador de exepciones 
@app.errorhandler(404)
def paginano(e):
    return'Revisa tu sintaxis, no encontre nada'

if __name__=='__main__':
    app.run(port=3000, debug=True)