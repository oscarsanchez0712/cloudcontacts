from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = 'cloudcontacts2024'

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form.get('telefono', '')
        try:
            conn = get_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO contactos (nombre, correo, telefono) VALUES (%s, %s, %s)",
                    (nombre, correo, telefono)
                )
            conn.commit()
            conn.close()
            flash('Contacto guardado correctamente', 'success')
        except pymysql.err.IntegrityError:
            flash('El correo ya está registrado', 'error')
        except Exception as e:
            flash(f'Error de conexión: {str(e)}', 'error')
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM contactos ORDER BY fecha_registro DESC")
            contactos = cursor.fetchall()
        conn.close()
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        contactos = []
    return render_template('contacts.html', contactos=contactos)

if __name__ == '__main__':
    app.run(debug=True)
