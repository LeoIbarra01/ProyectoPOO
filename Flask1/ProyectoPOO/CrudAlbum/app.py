from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'albums'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM albums')
        consultaA = cursor.fetchall()
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(e)
        flash('Error al recuperar los álbumes')
    return render_template('index.html')

@app.route('/guardarAlbum', methods=['POST'])
def guardarAlbum():
    if request.method == 'POST':
        Ftitulo = request.form['txtTitulo']
        Fartista = request.form['txtArtista']
        Fanio = request.form['txtAnio']
        file = request.files.get('cover')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            cover_path = filename  # Solo el nombre del archivo
        else:
            cover_path = None
            flash('Archivo no válido o no seleccionado')

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO albums (titulo, artista, anio, portada) VALUES (%s, %s, %s, %s)', 
                       (Ftitulo, Fartista, Fanio, cover_path))
        mysql.connection.commit()
        flash('Álbum guardado correctamente')
        return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM albums WHERE idAlbum=%s', (id,))
    albumE = cursor.fetchone()
    return render_template('editar.html', album=albumE)

@app.route('/ActualizarAlbum/<id>', methods=['POST'])
def ActualizarAlbum(id):
    if request.method == 'POST':
        Ftitulo = request.form['txtTitulo']
        Fartista = request.form['txtArtista']
        Fanio = request.form['txtAnio']
        file = request.files.get('cover')
        
        cursor = mysql.connection.cursor()

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            cover_path = filename  # Solo el nombre del archivo
            cursor.execute('UPDATE albums SET titulo=%s, artista=%s, anio=%s, portada=%s WHERE idAlbum=%s', 
                           (Ftitulo, Fartista, Fanio, cover_path, id))
        else:
            cursor.execute('UPDATE albums SET titulo=%s, artista=%s, anio=%s WHERE idAlbum=%s', 
                           (Ftitulo, Fartista, Fanio, id))
        
        mysql.connection.commit()
        flash('Álbum actualizado correctamente')
        return redirect(url_for('index'))

@app.route('/EliminarAlbum/<id>')
def EliminarAlbum(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM albums WHERE idAlbum=%s', (id,))
    mysql.connection.commit()
    flash('Álbum eliminado correctamente')
    return redirect(url_for('index'))

@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis, no encontré nada'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
