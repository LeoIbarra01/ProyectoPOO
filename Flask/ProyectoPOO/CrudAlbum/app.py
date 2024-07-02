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
    try:
        cursor= mysql.connection.cursor();
        cursor.execute('select * from albums')
        consultaA= cursor.fetchall()
        #print(consultaA)
        return render_template('index.html', albums= consultaA)


    except Exception as e:
        print(e)
        


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
    

@app.route('/editar/<id>')
def editar(id):
        cursor = mysql.connection.cursor()
        cursor.execute('select * from albums where idAlbum=%s', (id))
        albumE= cursor.fetchone()
        return render_template('editar.html', album=albumE)
    
    

@app.route('/ActualizarAlbum/<id>', methods=['POST'])
def ActualizarAlbum(id):
    if request.method == 'POST':
        # Tomamos los datos que vienen por POST
        Ftitulo = request.form['txtTitulo']
        Fartista = request.form['txtArtista']
        Fanio = request.form['txtAnio']
        # Enviamos a la BD sin incluir la columna de clave primaria
        cursor = mysql.connection.cursor()
        cursor.execute('update albums set titulo= %s ,artista=%s, anio=%s where idAlbum= %s',  (Ftitulo,Fartista, Fanio, id))
        mysql.connection.commit()
        flash('Álbum actualizado correctamente')
        return redirect(url_for('index'))
    
@app.route('/EliminarAlbum/<id>')
def EliminarAlbum(id):
    
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM albums WHERE idAlbum = %s', (id,))
    mysql.connection.commit()
    flash('Álbum eliminado correctamente')

    return redirect(url_for('index'))


    


#Manejador de exepciones 
@app.errorhandler(404)
def paginano(e):
    return'Revisa tu sintaxis, no encontre nada'

if __name__=='__main__':
    app.run(port=3000, debug=True)