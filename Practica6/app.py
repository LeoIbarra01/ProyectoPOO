from flask import Flask, request,render_template,url_for,redirect,flash
from flask_mysqldb import MySQL


app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='tbmedicos'
mysql= MySQL(app)

app.secret_key='mysecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registroMedico', methods=['GET'])
def registroMedico():
    if request.method == 'GET':
        # Tomamos los datos que vienen por POST
        Frfc = request.form['txtRfc']
        Fnombre = request.form['txtNombre']
        Fcedula = request.form['txtCedula']
        Fcorreo = request.form['txtCorreo']
        Fpassword = request.form['txtPassword']
        Frol = request.form['txtRol']

        
        # Enviamos a la BD sin incluir la columna de clave primaria
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO tbmedicos(RFC, Nom_Completo, Cedula, correro, password, ROL) VALUES (%s, %s, %s,%s, %s, %s)', (Frfc, Fnombre, Fcedula, Fcorreo, Fpassword, Frol))
        mysql.connection.commit()
        flash('Registro Guardado Correctamente')
        return redirect(url_for('formulario'))



#Manejador de exepciones 
@app.errorhandler(404)
def paginano(e):
    return'Revisa tu sintaxis, no encontre nada'

if __name__=='__main__':
    app.run(port=3000, debug=True)