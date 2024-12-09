from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

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
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  # Usuario de MySQL
        password='',  # Contraseña de MySQL
        database='servitec1'  # Nombre de la base de datos
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(user['id_usuario'], user['nombre'], user['id_rol'])
    return None

# Ruta para la página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        
        # Conectar a la base de datos
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='servitec1'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (nombre,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Verificar si el usuario existe y la contraseña en texto plano es correcta
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
        return render_template('admin_menu.html')
    return redirect(url_for('login'))

# Ruta para el menú del técnico
@app.route('/tecnico_menu')
@login_required
def tecnico_menu():
    if current_user.id_rol == 2:
        return render_template('tecnico_menu.html')
    return redirect(url_for('login'))

# Ruta para el menú del cliente
@app.route('/cliente_menu')
@login_required
def cliente_menu():
    if current_user.id_rol == 3:
        return render_template('cliente_menu.html')
    return redirect(url_for('login'))

# Ruta para agregar usuarios (solo admin)
@app.route('/', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.id_rol != 1:  # Solo el admin puede agregar usuarios
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']
        id_rol = request.form['id_rol']

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='servitec1'
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, contrasena, telefono, id_rol) VALUES (%s, %s, %s, %s, %s)",
            (nombre, email, contrasena, telefono, id_rol)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuario agregado correctamente', 'success')
        return redirect(url_for('admin_menu'))

    return render_template('add_user.html')

# Ruta para mostrar usuarios (solo admin)
@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.id_rol != 1:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('usuarios.html', users=users)

# Ruta para actualizar usuario (solo admin)
@app.route('/update_user/<int:id>', methods=['GET', 'POST'])
@login_required
def update_user(id):
    if current_user.id_rol != 1:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id,))
    user = cursor.fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        telefono = request.form['telefono']
        id_rol = request.form['id_rol']

        cursor.execute(
            "UPDATE usuarios SET nombre = %s, email = %s, contrasena = %s, telefono = %s, id_rol = %s WHERE id_usuario = %s",
            (nombre, email, contrasena, telefono, id_rol, id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios'))

    cursor.close()
    conn.close()
    return render_template('update_user.html', user=user)

# Ruta para eliminar usuario (solo admin)
@app.route('/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    if current_user.id_rol != 1:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('usuarios'))

# Ruta para las órdenes
@app.route('/ordenes')
@login_required
def ordenes():
    if current_user.id_rol != 1:  # Solo el admin puede ver las órdenes
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ordenes")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('ordenes.html', orders=orders)

# Ruta para pagos
@app.route('/pagos')
@login_required
def pagos():
    if current_user.id_rol != 1:  # Solo el admin puede ver los pagos
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pagos")
    payments = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('pagos.html', payments=payments)

# Ruta para asignar técnico a una orden
@app.route('/asignar_tecnico/<int:id_orden>', methods=['GET', 'POST'])
@login_required
def asignar_tecnico(id_orden):
    if current_user.id_rol != 1:  # Solo el admin puede asignar técnicos
        return redirect(url_for('login'))

    if request.method == 'POST':
        id_tecnico = request.form['id_tecnico']
        fecha_ingreso = request.form['fecha_ingreso']
        monto = request.form['monto']

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='servitec1'
        )
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ordenes SET id_tecnico = %s, f_ingreso = %s, monto = %s WHERE id_orden = %s",
            (id_tecnico, fecha_ingreso, monto, id_orden)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Técnico y monto asignados correctamente', 'success')
        return redirect(url_for('ordenes'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id_rol = 2")  # Técnicos
    technicians = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('asignar_tecnico.html', technicians=technicians, id_orden=id_orden)

# Órdenes asignadas al técnico
@app.route('/ordenes_asignadas')
@login_required
def ordenes_asignadas():
    if current_user.id_rol != 2:  # Solo técnicos pueden ver esta página
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ordenes WHERE id_tecnico = %s", (current_user.id_usuario,))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('ordenes_asignadas.html', orders=orders)

# Actualizar estado de la orden
@app.route('/actualizar_estado/<int:id_orden>', methods=['GET', 'POST'])
@login_required
def actualizar_estado(id_orden):
    if current_user.id_rol != 2:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        estado = request.form['estado']
        cursor.execute("UPDATE ordenes SET estado = %s WHERE id_orden = %s", (estado, id_orden))
        conn.commit()
        flash('Estado actualizado correctamente', 'success')
        return redirect(url_for('ordenes_asignadas'))

    cursor.execute("SELECT * FROM ordenes WHERE id_orden = %s", (id_orden,))
    order = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('actualizar_estado.html', order=order)

# Inventario
@app.route('/inventario', methods=['GET', 'POST'])
@login_required
def inventario():
    if current_user.id_rol != 2:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM inventario")
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('inventario.html', items=items)

# Reducir cantidad del inventario
@app.route('/reducir_inventario/<int:id_item>', methods=['POST'])
@login_required
def reducir_inventario(id_item):
    if current_user.id_rol != 2:
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE inventario SET cantidad = cantidad - 1 WHERE id_item = %s AND cantidad > 0", (id_item,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Cantidad actualizada correctamente', 'success')
    return redirect(url_for('inventario'))

# Ruta para solicitar servicio técnico
@app.route('/servicio_tecnico', methods=['GET', 'POST'])
@login_required
def servicio_tecnico():
    if current_user.id_rol != 3:
        return redirect(url_for('login'))

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        marca = request.form['marca']

        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='servitec1'
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ordenes (id_cliente, descripcion, marca, estado) VALUES (%s, %s, %s, 'Pendiente')",
            (current_user.id_usuario, descripcion, marca)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash('Solicitud enviada correctamente', 'success')
        return redirect(url_for('cliente_menu'))

    return render_template('servicio_tecnico.html')



# Ruta para ver deudas del cliente
@app.route('/deudas')
@login_required
def deudas():
    if current_user.id_rol != 3:  # Solo los clientes pueden ver esta página
        return redirect(url_for('login'))

    # Conectar a la base de datos
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    
    # Obtener todas las órdenes de este cliente
    cursor.execute("""
        SELECT o.id_orden, o.descripcion, o.marca, o.monto, p.monto_pagado AS monto_pagado, u.nombre AS tecnico_nombre
        FROM ordenes o
        LEFT JOIN pagos p ON o.id_orden = p.id_orden
        LEFT JOIN usuarios u ON o.id_tecnico = u.id_usuario
        WHERE o.id_cliente = %s
    """, (current_user.id_usuario,))
    
    deudas = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('deudas.html', deudas=deudas)
# Ruta para ver órdenes del cliente
@app.route('/mis_ordenes')
@login_required
def mis_ordenes():
    if current_user.id_rol != 3:  # Solo clientes pueden ver esta página
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM ordenes WHERE id_cliente = %s",
        (current_user.id_usuario,)
    )
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('mis_ordenes.html', orders=orders)

@app.route('/update_order_status/<int:id_orden>', methods=['GET', 'POST'])
@login_required
def update_order_status(id_orden):
    if current_user.id_rol != 2:  # Aseguramos que solo los técnicos acceden a esta ruta
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ordenes WHERE id_orden = %s", (id_orden,))
    order = cursor.fetchone()

    if not order:
        flash('Orden no encontrada.', 'error')
        return redirect(url_for('tecnico_menu'))

    if request.method == 'POST':
        estado = request.form['estado']
        cursor.execute(
            "UPDATE ordenes SET estado = %s WHERE id_orden = %s",
            (estado, id_orden)
        )
        conn.commit()
        flash('Estado de la orden actualizado.', 'success')
        return redirect(url_for('ordenes_asignadas'))

    cursor.close()
    conn.close()
    return render_template('update_order_status.html', order=order)

@app.route('/actualizar_fecha_entrega_tecnico/<int:id_orden>', methods=['GET', 'POST'])
@login_required
def actualizar_fecha_entrega_tecnico(id_orden):
    if current_user.id_rol != 2:  # Solo los técnicos pueden actualizar la fecha de entrega
        return redirect(url_for('login'))

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='servitec1'
    )
    cursor = conn.cursor(dictionary=True)

    # Verificar si la orden está asignada al técnico actual
    cursor.execute("SELECT * FROM ordenes WHERE id_orden = %s AND id_tecnico = %s", (id_orden, current_user.id_usuario))
    order = cursor.fetchone()

    if not order:
        flash('No tienes permiso para actualizar esta orden.', 'error')
        cursor.close()
        conn.close()
        return redirect(url_for('tecnico_menu'))

    if request.method == 'POST':
        f_entrega = request.form['f_entrega']

        cursor.execute(
            "UPDATE ordenes SET f_entrega = %s WHERE id_orden = %s",
            (f_entrega, id_orden)
        )
        conn.commit()
        flash('Fecha de entrega actualizada correctamente', 'success')
        cursor.close()
        conn.close()
        return redirect(url_for('ordenes_asignadas'))

    cursor.close()
    conn.close()
    return render_template('actualizar_fecha_entrega_tecnico.html', id_orden=id_orden)

# Ruta para cerrar sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)