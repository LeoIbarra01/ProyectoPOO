from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
# Datos de usuarios (simulados)
usuarios = {
    "miRFC": "miContraseña",
    # Agrega más usuarios si es necesario
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    rfc = request.form['rfc']
    password = request.form['password']
    
    if rfc in usuarios and usuarios[rfc] == password:
        # Autenticación exitosa
        return redirect(url_for('inicio_exitoso'))
    else:
        # Autenticación fallida
        return render_template('index.html', error='RFC o contraseña incorrectos')

@app.route('/inicio_exitoso')
def inicio_exitoso():
    return '¡Inicio de sesión exitoso!'

if __name__ == '__main__':
    app.run(debug=True)
