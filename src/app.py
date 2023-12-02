from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
import os

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://example.com"}})



from config import config

app=Flask(__name__)

conexion=MySQL(app)

@app.route('/usuario', methods=['GET'])
def listar_usuarios():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * from Usuario"
        cursor.execute(sql)
        datos=cursor.fetchall()
        usuarios=[]
        for fila in datos:
            usuario={'idDocumento':fila[0],'Nombre1':fila[1],'Nombre2':fila[2],'Apellido1':fila[3],'Apellido2':fila[4],'CorreoElectronico':fila[5],'Direccion':fila[6],'RolUsuario_idRolUsuarioNombre':fila[7],'TipodeDocumento_idTipodeDocumento':fila[8],'Contraseña':fila[9]}
            usuarios.append(usuario)
        return jsonify({'usuarios': usuarios, 'mensaje': 'Usuarios listados.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

@app.route('/usuario/<idDocumento>',methods=['GET'])
def leer_usuario(idDocumento):
    cursor=conexion.connection.cursor()
    sql="SELECT * from Usuario WHERE idDocumento = '{0}'".format(idDocumento)
    cursor.execute(sql)
    datos=cursor.fetchone()
    if datos != None:
        usuario={'idDocumento':datos[0],'Nombre1':datos[1],'Nombre2':datos[2],'Apellido1':datos[3],'Apellido2':datos[4],'CorreoElectronico':datos[5],'Direccion':datos[6],'RolUsuario_idRolUsuarioNombre':datos[7],'TipodeDocumento_idTipodeDocumento':datos[8],'Contraseña':datos[9]}
        return jsonify({'usuarios': usuario, 'mensaje': 'Usuario encontrado.'})
    else: 
        return jsonify({'mensaje':'Error usuario no encontrado'})

def pagina_no_encontrada(error):
    return '<h1>La pagina que intentas buscar no existe..</h1>',404
#------------
@app.route('/obtener_discapacidades', methods=['GET'])
def obtener_todas_discapacidades():
    cursor = conexion.connection.cursor()
    sql = "SELECT * FROM Discapacidad"
    cursor.execute(sql)
    datos = cursor.fetchall()

    discapacidades = []
    for dato in datos:
        discapacidad = {
            'idDiscapacidad': dato[0],
            'nombre': dato[1],
            'descripcion': dato[2],
             'imagen': dato[3].decode('utf-8') if dato[3] else None  # Supongo que la imagen es una URL o ruta de archivo
        }
        discapacidades.append(discapacidad)

    if discapacidades:
        return jsonify({'discapacidades': discapacidades, 'mensaje': 'Discapacidades encontradas.'})
    else:
        return jsonify({'mensaje': 'Error: No se encontraron discapacidades.'})
#------------
#registro usuario
@app.route('/usuarioregistrar',methods=['POST'])
def registrar_usuario():
    try:
        idDocumento = request.form['idDocumento']
        Nombre1 = request.form['Nombre1']
        Nombre2 = request.form['Nombre2']
        Apellido1 = request.form['Apellido1']
        Apellido2 = request.form['Apellido2']
        CorreoElectronico = request.form['CorreoElectronico']
        Direccion = request.form['Direccion']
        RolUsuario_idRolUsuarioNombre = request.form['RolUsuario_idRolUsuarioNombre']
        TipodeDocumento_idTipodeDocumento = request.form['TipodeDocumento_idTipodeDocumento']
        Contraseña = request.form['Contraseña']

        #lógica para manejar los datos recibidos

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Usuario (idDocumento, Nombre1, Nombre2, Apellido1, Apellido2, CorreoElectronico, Direccion, RolUsuario_idRolUsuarioNombre, TipodeDocumento_idTipodeDocumento, Contraseña) 
                 VALUES ('{0}', '{1}', '{2}','{3}', '{4}', '{5}','{6}', '{7}', '{8}','{9}')""".format(idDocumento, Nombre1, Nombre2, Apellido1, Apellido2, CorreoElectronico, Direccion, RolUsuario_idRolUsuarioNombre, TipodeDocumento_idTipodeDocumento, Contraseña)
        cursor.execute(sql)
        conexion.connection.commit()

        return jsonify({"mensaje": "Usuario registrado"})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al registrar usuario'})
#--------------------
#@app.route('/discapacidad',methods=['POST'])
#def registrar_discapacidad():
    #print(request.json)
#    try:
#        cursor=conexion.connection.cursor()
#        sql="""INSERT INTO Discapacidad (Nombre,Descripcion) 
#        VALUES ('{0}','{1}')""".format(request.json['Nombre'],request.json['Descripcion'])
#        cursor.execute(sql)
#        conexion.connection.commit()#confima la accion de insercion
#        return jsonify({"mensaje":"discapacidad registrado"})
#    except Exception as ex:
#        return jsonify({'mensaje':'Error discapacidad no registrado'})
#-------------------
#Registro Discapacidad
@app.route('/discapacidad', methods=['POST'])
def registrar_discapacidad():
    try:
        nombre = request.form['Nombre']
        descripcion = request.form['Descripcion']
        imagen = request.files['Imagen']  # Accede al archivo de imagen enviado

        # Verifica si se envió una imagen y tiene un nombre de archivo válido
        if imagen and imagen.filename != '':
            # Guarda la imagen en una carpeta, asegúrate de que la carpeta exista
            ruta_guardado = './imagenes'
            if not os.path.exists(ruta_guardado):
                os.makedirs(ruta_guardado)
            ruta_imagen = os.path.join(ruta_guardado, imagen.filename)
            imagen.save(ruta_imagen)

            # Guarda los datos en la base de datos
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO Discapacidad (Nombre, Descripcion,Imagen) 
                     VALUES ('{0}', '{1}', '{2}')""".format(nombre, descripcion, ruta_imagen)
            cursor.execute(sql)
            conexion.connection.commit()
            
            return jsonify({"mensaje": "Discapacidad registrada con imagen"})
        else:
            return jsonify({"mensaje": "Error: no se envió ninguna imagen"})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al registrar la discapacidad'})
#    ----------------------------------------- 
#registro usuario
@app.route('/registrar_rutina',methods=['POST'])
def registrar_rutina():
    try:
        Nombre_Ejercicio = request.form['Nombre_Ejercicio']
        DuracionMin = request.form['DuracionMin']
        Series = request.form['Series']
        RepeticionesPorSerie = request.form['RepeticionesPorSerie']
        Descripcion = request.form['Descripcion']
        Imagen1 =request.files['Imagen1']
        Imagen2 =request.files['Imagen2']
        Imagen3 =request.files['Imagen3']
        Discapacidad_idDiscapacidad = request.form['Discapacidad_idDiscapacidad']
        
        #lógica para manejar los datos recibidos
        if Imagen1 and Imagen2 and Imagen3:
            Imagen1.save('../imagenes')  # Guardar la imagen 1
            Imagen2.save('../imagenes')  # Guardar la imagen 2
            Imagen3.save('../imagenes') 

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Rutina (Nombre_Ejercicio,DuracionMin,Series,RepeticionesPorSerie,Descripcion,Discapacidad_idDiscapacidad)
                 VALUES ('{0}', '{1}', '{2}','{3}', '{4}', '{5}','{6}', '{7}', '{8}')""".format(Nombre_Ejercicio, DuracionMin, Series, RepeticionesPorSerie, Descripcion,Imagen1,Imagen2,Imagen3,Discapacidad_idDiscapacidad)
        cursor.execute(sql)
        conexion.connection.commit()

        return jsonify({"mensaje": "Rutina registrada"})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al registrar rutina'})
#--------------------
#@app.route('/rutina',methods=['POST'])
#def registrar_rutina():
    #print(request.json)
#    try:
#        cursor=conexion.connection.cursor()
#        sql="""INSERT INTO Rutina (Nombre_Ejercicio,DuracionMin,Series,RepeticionesPorSerie,Descripcion,Discapacidad_idDiscapacidad)
#        VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')""".format(request.json['Nombre_Ejercicio'],request.json['DuracionMin'],request.json['Series'],request.json['RepeticionesPorSerie'],request.json['Descripcion'],request.json['Discapacidad_idDiscapacidad'])
#        cursor.execute(sql)
#        conexion.connection.commit()#confima la accion de insercion
#        return jsonify({"mensaje":"rutina registrado"})
#    except Exception as ex:
#        return jsonify({'mensaje':'Error rutina no registrado'})
#-------------

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

