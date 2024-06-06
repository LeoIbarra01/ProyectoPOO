from flask import Flask, request,render_template,jsonify
from flask_mysqldb import MySQL


app= Flask(__name__)
app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='bdflask'
mysql= MySQL(app)

@app.route('/pruebaConexion')
def pruebaConexion():
    try:
        cursor=mysql.connection.cursor()
        cursor.execute("Select 1")
        datos=cursor.fetchone()
        return jsonify({'status': 'conexion exitosa', 'data':datos})
    except Exception as ex:
       return jsonify({'status': 'Error de conexion', 'mensaje':str(ex)})

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/formulario', methods=['GET'])
def formulario():
   if request.method=='GET':
       titulo= request.form['txtTitulo']
       artista= request.form['txtArtista']
       anio= request.form['txtAnio']
       print(titulo, artista, anio)
       return 'Datos recibidos en el server'
   

@app.route('/hi/<numero>')
def hi(numero):
    return 'numero '+numero+'!!!'

#Manejador de exepciones 


if __name__=='__main__':
    app.run(port=3000, debug=True)