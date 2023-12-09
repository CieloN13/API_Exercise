from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
import os
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from base64 import encodebytes
from datetime import datetime

from flask_cors import CORS,cross_origin

app = Flask(__name__)

CORS(app)


from config import config

app=Flask(__name__)

conexion=MySQL(app)
#login
@app.route('/validar_usuario', methods=['POST'])
@cross_origin()
def validar_usuario():
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        contraseña = data.get('contraseña')

        cursor = conexion.connection.cursor()
        sql = "SELECT idDocumento, Contraseña, RolUsuario_idRolUsuarioNombre FROM Usuario WHERE idDocumento=%s"
        cursor.execute(sql, (usuario,))
        usuario_data = cursor.fetchone()

        if usuario_data:
            id_documento, hash_contraseña, id_rol = usuario_data
            if check_password_hash(hash_contraseña, contraseña):
                return jsonify({'idRol': id_rol, 'mensaje': 'Usuario validado correctamente'})
            else:
                return jsonify({'mensaje': 'Credenciales inválidas'}), 401  # Unauthorized
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404  # Not Found
    except Exception as ex:
        return jsonify({'mensaje': 'Error en la validación del usuario'}), 500  # Internal Server Error
#--------------
#listar usuarios
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
#listar usuario por id
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
#obtener discapacidades
@app.route('/obtener_discapacidades', methods=['GET'])
@cross_origin()
def obtener_todas_discapacidades():
    try:
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
                'imagen': dato[3].decode('utf-8') if dato[3] else None
            }
            discapacidades.append(discapacidad)

        if discapacidades:
            return jsonify({'discapacidades': discapacidades, 'mensaje': 'Discapacidades encontradas.'})
        else:
            return jsonify({'mensaje': 'Error: No se encontraron discapacidades.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en la obtención de discapacidades: ' + str(e)})
#------------
#registro usuario
@app.route('/usuarioregistrar',methods=['POST'])
@cross_origin()
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
@cross_origin()
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
#Registro rutinas
@app.route('/registrar_rutina',methods=['POST'])
@cross_origin()
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
            ruta_guardado = './imagenes'
            if not os.path.exists(ruta_guardado):
                os.makedirs(ruta_guardado)

            nombre_imagen1 = secure_filename(Imagen1.filename)
            nombre_imagen2 = secure_filename(Imagen2.filename)
            nombre_imagen3 = secure_filename(Imagen3.filename)

            ruta_imagen1 = os.path.join(ruta_guardado, nombre_imagen1)
            ruta_imagen2 = os.path.join(ruta_guardado, nombre_imagen2)
            ruta_imagen3 = os.path.join(ruta_guardado, nombre_imagen3)

            Imagen1.save(ruta_imagen1)  # Guardar la imagen 1
            Imagen2.save(ruta_imagen2)  # Guardar la imagen 2
            Imagen3.save(ruta_imagen3) 

            with open(ruta_imagen1, 'rb') as img_file1:
                binary_data1 = encodebytes(img_file1.read()).decode('utf-8')
            with open(ruta_imagen2, 'rb') as img_file2:
                binary_data2 = encodebytes(img_file2.read()).decode('utf-8')
            with open(ruta_imagen3, 'rb') as img_file3:
                binary_data3 = encodebytes(img_file3.read()).decode('utf-8')

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Rutina (Nombre_Ejercicio,DuracionMin,Series,RepeticionesPorSerie,Descripcion,Imagen1,Imagen2,Imagen3,Discapacidad_idDiscapacidad)
                 VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')""".format(Nombre_Ejercicio, DuracionMin, Series, RepeticionesPorSerie, Descripcion,binary_data1,binary_data2,binary_data3,Discapacidad_idDiscapacidad)
        cursor.execute(sql)
        conexion.connection.commit()

        return jsonify({"mensaje": "Rutina registrada"})
    except Exception as ex:
        return jsonify({'mensaje': 'Error al registrar rutina'})
#--------------------
#registrar Notificacion
@app.route('/subir_notificacion', methods=['POST'])
@cross_origin()
def subir_notificacion():
    try:
        # Obtener los datos del formulario o cuerpo de la solicitud
        descripcion = request.form['Descripcion']
        fecha_notificacion = request.form['Fecha']
        nombre = request.form['Nombre']
        
        if descripcion is None or fecha_notificacion is None or nombre is None:
            raise ValueError('Datos incompletos')

        # Convertir la fecha a un objeto datetime si es necesario
        fecha_notificacion = datetime.strptime(fecha_notificacion, '%Y-%m-%d')

        # Realizar la inserción en la base de datos
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Notificacion(Descripcion,FechaNotificacion,Nombre)
                 VALUES ('{0}', '{1}', '{2}')""".format(descripcion, fecha_notificacion, nombre)
        cursor.execute(sql)
        conexion.connection.commit()

        return jsonify({"mensaje": "Notificación subida correctamente"})
    except Exception as ex:
        error_msg = f'Error al subir la notificación: {str(ex)}. Datos recibidos: Descripcion={request.form.get("Descripcion")}, FechaNotificacion={request.form.get("FechaNotificacion")}, Nombre={request.form.get("Nombre")}'
        return jsonify({'mensaje': error_msg})


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

