from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.datastructures import RequestCacheControl

app = Flask(__name__)
#Conexion a base de datos con los siguientes datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'DiegoAlejandro'
app.config['MYSQL_PASSWORD'] = '.Php1624.'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

#Configuraciones
app.secret_key = 'mysecretkey'


#La siguiente es indicar que cada vez que un usuario entre a nuestra ruta principal de nuestra aplicacion, vamos a responderle algo
@app.route('/')
def Index():
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM contacts')
   data = cur.fetchall()
   return render_template('index.html', contacts = data)
#Creacion de otra ruta para agregar contactos, @app.route es para creacion de rutas
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Documento = request.form['Documento']
        Perfil = request.form['Perfil']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (Nombre, Documento, Perfil) VALUES (%s, %s, %s)', (Nombre, Documento, Perfil))
        mysql.connection.commit()
        flash('Cliente agregado correctamente')
        return redirect(url_for('Index'))
#def - se define una funcion que retorna inicialmente un texto
@app.route('/Editar/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Documento = request.form['Documento']
        Perfil = request.form['Perfil']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET Nombre = %s,
                Documento = %s,
                Perfil = %s
            WHERE id = %s
        """, (Nombre, Documento, Perfil, id))
        mysql.connection.commit()
        flash('Contacto Actualizado')
        return redirect(url_for('index.html'))

@app.route('/Borrar/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto Borrado Satisfactoriamente')
    return redirect(url_for('Index'))


#llamar al puerto y con debug los cambios que se hagan en el servidor los reinicia automaticamente
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
#Lineas anteriores son para iniciar un servidor
