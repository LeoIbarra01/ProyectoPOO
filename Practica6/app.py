from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'medicos'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/formulario')
def formulario():
    return render_template('formulario.html')


@app.route('/registrarMedico', methods=['POST'])
def registrarMedico():
    if request.method == 'POST':
        # Tomamos los datos que vienen por POST
        Frfc = request.form['txtRfc']
        Fnombre = request.form['txtNombre']
        Fcedula = request.form['txtCedula']
        Fcorreo = request.form['txtCorreo']
        Fpassword = request.form['txtPassword']
        Frol = request.form['txtRol']
        
        # Enviamos a la BD sin incluir la columna de clave primaria
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tbmedicos1(RFC, Nombre, Cedula, Correo, Password, Rol) VALUES (%s, %s, %s, %s, %s, %s)', (Frfc, Fnombre, Fcedula, Fcorreo, Fpassword, Frol))
        mysql.connection.commit()
        flash('Registro Guardado Correctamente')
        return redirect(url_for('formulario'))


@app.route('/consultarMedicos')
def consultarMedicos():
    try:
        cursor= mysql.connection.cursor();
        cursor.execute('select * from tbmedicos1')
        consultaA= cursor.fetchall()
        #print(consultaA)
        return render_template('consultarMedicos.html', tbmedicos1= consultaA)


    except Exception as e:
        print(e)
        


    return render_template('consultarMedicos.html')

# Manejador de excepciones
@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis, no encontré nada'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
