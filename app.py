from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configurar conexión a la base de datos MySQL
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Usuario de MySQL
        password='',  # Contraseña de MySQL
        database='servitec1'  # Nombre de la base de datos
    )
    return conn

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, id_usuario, nombre, id_rol):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.id_rol = id_rol

    @property
    def id(self):
        return self.id_usuario

# Cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(user['id_usuario'], user['nombre'], user['id_rol'])
    return None

# Ruta principal que redirige a /login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        
        # Conectar a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        # Verificar si el usuario existe y la contraseña coincide (en texto plano)
        if user and user['contrasena'] == contrasena:
            # Autenticar al usuario
            user_obj = User(user['id_usuario'], user['nombre'], user['id_rol'])
            login_user(user_obj)
            # Redirigir según el rol
            if user['id_rol'] == 1:
                return redirect(url_for('admin_menu'))
            elif user['id_rol'] == 2:
                return redirect(url_for('tecnico_menu'))
            elif user['id_rol'] == 3:
                return redirect(url_for('cliente_menu'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

# Ruta para el menú del administrador
@app.route('/admin_menu')
@login_required
def admin_menu():
    if current_user.id_rol == 1:
        return render_template('admin_menu.html', nombre=current_user.nombre)
    return redirect(url_for('login'))

# Ruta para el menú del técnico
@app.route('/tecnico_menu')
@login_required
def tecnico_menu():
    if current_user.id_rol == 2:
        return render_template('tecnico_menu.html', nombre=current_user.nombre)
    return redirect(url_for('login'))

# Ruta para el menú del cliente
@app.route('/cliente_menu')
@login_required
def cliente_menu():
    if current_user.id_rol == 3:
        return render_template('cliente_menu.html', nombre=current_user.nombre)
    return redirect(url_for('login'))

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)