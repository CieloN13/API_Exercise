from flask import Flask,jsonify,request,url_for,send_file,abort
from flask_mysqldb import MySQL
import os
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from base64 import encodebytes
from datetime import datetime

from flask_cors import CORS,cross_origin


from flask import send_from_directory



app = Flask(__name__)

CORS(app)


from config import config
conexion=MySQL(app)

#login
@app.route('/obtener_usuarios', methods=['GET'])
@cross_origin()
def obtener_todos_usuarios():
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT idDocumento, Contraseña
            FROM Usuario
        """
        cursor.execute(sql)
        datos = cursor.fetchall()

        usuarios = []
        for dato in datos:
            usuario = {
                'idDocumento': dato[0],
                'Contraseña': dato[1]
            }
            usuarios.append(usuario)

        if usuarios:
            return jsonify({'usuarios': usuarios, 'mensaje': 'Usuarios encontrados.'})
        else:
            return jsonify({'mensaje': 'Error: No se encontraron usuarios.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en la obtención de usuarios: ' + str(e)})
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
@app.route('/obtener_datos_usuario/<int:idDocumento>', methods=['GET'])
@cross_origin()
def obtener_datos_usuario(idDocumento):
    try:
        cursor = conexion.connection.cursor()

        sql = "SELECT Nombre1, Nombre2, Apellido1, Apellido2, CorreoElectronico FROM Usuario WHERE idDocumento = %s"
        cursor.execute(sql, (idDocumento,))
        usuario = cursor.fetchone()

        if usuario:
            datos_usuario = {
                'nombre1': usuario[0],
                'nombre2': usuario[1],
                'apellido1': usuario[2],
                'apellido2': usuario[3],
                'correoElectronico': usuario[4]
            }
            return jsonify(datos_usuario)
        else:
            return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': 'Error al obtener los datos del usuario: ' + str(e)}), 500
#listar notificaciones
@app.route('/obtener_notificaciones', methods=['GET'])
@cross_origin()
def obtener_todas_notificaciones():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM notificacion"
        cursor.execute(sql)
        datos = cursor.fetchall()

        notificaciones = []
        if datos:
            for dato in datos:
                notificacion = {
                    'idNotificacion': dato[0],
                    'descripcion': dato[1],
                    'fechaNotificacion': dato[2],
                    'nombre': dato[3]
                }
                notificaciones.append(notificacion)
        else:
            # Si no se encuentran notificaciones, se agrega una notificación predeterminada
            notificacion_predeterminada = {
                'idNotificacion': -1,
                'descripcion': 'No se encontraron notificaciones',
                'fechaNotificacion': None,
                'nombre': 'Notificación predeterminada'
            }
            notificaciones.append(notificacion_predeterminada)

        if notificaciones:
            return jsonify({'notificaciones': notificaciones, 'mensaje': 'Notificaciones encontradas.'})
        else:
            return jsonify({'mensaje': 'Error: No se encontraron notificaciones.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en la obtención de notificaciones: ' + str(e)})
#--------------------------------------------------------------------------------------------------------
#obtener rutinas
@app.route('/obtener_rutinas', methods=['GET'])
@cross_origin()
def obtener_rutinas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT idRutina, Nombre_Ejercicio, DuracionMin, Series, RepeticionesPorSerie, Descripcion FROM Rutina"
        cursor.execute(sql)
        datos = cursor.fetchall()

        rutinas = []
        for dato in datos:
            rutina = {
                'idRutina': dato[0],
                'nombreEjercicio': dato[1],
                'duracionMin': dato[2],
                'series': dato[3],
                'repeticionesPorSerie': dato[4],
                'descripcion': dato[5],
            }
            rutinas.append(rutina)

        if rutinas:
            return jsonify({'rutinas': rutinas, 'mensaje': 'Rutinas encontradas.'})
        else:
            return jsonify({'mensaje': 'Error: No se encontraron rutinas.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en la obtención de rutinas: ' + str(e)})
#---------------------------
#obtener Rutinas por id
@app.route('/obtener_rutinas/<int:idDiscapacidad>', methods=['GET'])
@cross_origin()
def obtener_rutinas_por_discapacidad(idDiscapacidad):
    try:
        cursor = conexion.connection.cursor()
        sql = """
            SELECT Nombre_Ejercicio, DuracionMin, Series, RepeticionesPorSerie, Descripcion
            FROM Rutina
            WHERE Discapacidad_idDiscapacidad = %s
        """
        cursor.execute(sql, (idDiscapacidad,))
        datos = cursor.fetchall()

        rutinas = []
        if datos:
            for dato in datos:
                rutina = {
                    'Nombre_Ejercicio': dato[0],
                    'DuracionMin': dato[1],
                    'Series': dato[2],
                    'RepeticionesPorSerie': dato[3],
                    'Descripcion': dato[4]
                }
                rutinas.append(rutina)
        else:
            # Si no se encuentran rutinas, se agrega una rutina predeterminada
            rutina_predeterminada = {
                'Nombre_Ejercicio': 'No se encontraron rutinas',
                'DuracionMin': 0,
                'Series': 0,
                'RepeticionesPorSerie': 0,
                'Descripcion': 'No se encontraron rutinas por el momento, espera a que el administrador agregue una.'
            }
            rutinas.append(rutina_predeterminada)

        if rutinas:
            return jsonify({'rutinas': rutinas, 'mensaje': 'Rutinas encontradas.'})
        else:
            return jsonify({'mensaje': 'Error: No se encontraron rutinas para esta discapacidad.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error en la obtención de rutinas: ' + str(e)})
#-----------------------------------------------------------------------------------------------------------
def pagina_no_encontrada(error):
    return '<h1>La pagina que intentas buscar no existe..</h1>',404
#---------------------------------------------------------------------------------------------------------------
#obtener imagen
@app.route('/imagenes/<int:idDiscapacidad>', methods=['GET'])
@cross_origin()
def obtener_imagen_discapacidad(idDiscapacidad):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT imagen FROM Discapacidad WHERE idDiscapacidad = %s"
        cursor.execute(sql, (idDiscapacidad,))
        imagen = cursor.fetchone()
        
        if imagen is None:
            abort(404)  # Devuelve un código de estado 404 si no se encuentra ninguna imagen
        
        nombre_imagen = imagen[0]
        ruta_imagen = os.path.join('API_Exercise', 'imagenes', nombre_imagen)
        
        if not os.path.exists(ruta_imagen):
            abort(404)  # Devuelve un código de estado 404 si la imagen no existe en la ruta especificada
        
        return send_file(ruta_imagen, mimetype='image/jpeg')
    
    except Exception as e:
        # Maneja los errores según sea necesario
        return str(e), 500  # Devuelve un mensaje de error y un código de estado 500 si ocurre una excepción
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
                'imagen': dato[3]
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
#-------------------
#Registro Discapacidad
@app.route('/discapacidad', methods=['POST'])
@cross_origin()
def subir_discapacidad():
    try:
        # Obtener los datos del formulario o cuerpo de la solicitud
        nombre = request.form['Nombre']
        descripcion = request.form['Descripcion']
        
        if nombre is None or descripcion is None:
            raise ValueError('Datos incompletos')

        # Realizar la inserción en la base de datos
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Discapacidad(Nombre, Descripcion)
                 VALUES ('{0}', '{1}')""".format(nombre, descripcion)
        cursor.execute(sql)
        conexion.connection.commit()

        return jsonify({"mensaje": "Discapacidad registrada correctamente"})
    except Exception as ex:
        error_msg = f'Error al registrar la discapacidad: {str(ex)}. Datos recibidos: Nombre={request.form.get("Nombre")}, Descripcion={request.form.get("Descripcion")}'
        return jsonify({'mensaje': error_msg})
#    ----------------------------------------- 
#Registro rutinas
@app.route('/registrar_rutina', methods=['POST'])
@cross_origin()
def registrar_rutina():
    try:
        Nombre_Ejercicio = request.form['Nombre_Ejercicio']
        DuracionMin = request.form['DuracionMin']
        Series = request.form['Series']
        RepeticionesPorSerie = request.form['RepeticionesPorSerie']
        Descripcion = request.form['Descripcion']
        Discapacidad_idDiscapacidad = request.form['Discapacidad_idDiscapacidad']
        
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Rutina (Nombre_Ejercicio,DuracionMin,Series,RepeticionesPorSerie,Descripcion,Discapacidad_idDiscapacidad)
                 VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')""".format(Nombre_Ejercicio, DuracionMin, Series, RepeticionesPorSerie, Descripcion, Discapacidad_idDiscapacidad)
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
#-----------------------------------
#Eliminar discapacidades
@app.route('/eliminar_discapacidad_con_rutinas/<int:idDiscapacidad>', methods=['DELETE'])
@cross_origin()
def eliminar_discapacidad_con_rutinas(idDiscapacidad):
    try:
        cursor = conexion.connection.cursor()

        # Eliminar todas las rutinas asociadas a la discapacidad
        sql_eliminar_rutinas = "DELETE FROM Rutina WHERE Discapacidad_idDiscapacidad = %s"
        cursor.execute(sql_eliminar_rutinas, (idDiscapacidad,))
        
        # Eliminar la discapacidad
        sql_eliminar_discapacidad = "DELETE FROM Discapacidad WHERE idDiscapacidad = %s"
        cursor.execute(sql_eliminar_discapacidad, (idDiscapacidad,))

        conexion.connection.commit()

        return jsonify({'mensaje': 'Discapacidad y sus rutinas asociadas eliminadas correctamente.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error al eliminar la discapacidad y sus rutinas asociadas: ' + str(e)})
#-----------------
#Editar discapacidades
@app.route('/editar_discapacidad/<int:idDiscapacidad>', methods=['PUT'])
@cross_origin()
def editar_discapacidad(idDiscapacidad):
    try:
        data = request.json
        nuevo_nombre = data['nombre']
        nueva_descripcion = data['descripcion']
        
        cursor = conexion.connection.cursor()
        sql = """
            UPDATE Discapacidad
            SET nombre = %s, descripcion = %s
            WHERE idDiscapacidad = %s
        """
        cursor.execute(sql, (nuevo_nombre, nueva_descripcion, idDiscapacidad))
        conexion.connection.commit()

        return jsonify({'mensaje': 'Discapacidad editada exitosamente.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error al editar la discapacidad: ' + str(e)})
#-------------------
#Rutinas Editar
@app.route('/editar_rutina/<int:idRutina>', methods=['PUT'])
def editar_rutina(idRutina):
    try:
        data = request.json
        nuevo_nombre = data.get('nombre', '')
        nueva_descripcion = data.get('descripcion', '')
        nueva_duracion = data.get('duracion', 0)
        nueva_serie = data.get('series', 0)
        nuevas_repeticiones = data.get('repeticiones', 0)
        cursor = conexion.connection.cursor()

        sql = """
            UPDATE Rutina
            SET Nombre_Ejercicio = %s, Descripcion = %s, DuracionMin = %s, Series = %s, RepeticionesPorSerie = %s
            WHERE idRutina = %s
        """
        cursor.execute(sql, (nuevo_nombre, nueva_descripcion, nueva_duracion, nueva_serie, nuevas_repeticiones,idRutina))
        conexion.connection.commit()

        return jsonify({'mensaje': 'Rutina actualizada correctamente.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error al actualizar la rutina: ' + str(e)})
#------------------------
#Rutinas Eliminar
@app.route('/eliminar_rutina/<int:idRutina>', methods=['DELETE'])
def eliminar_rutina(idRutina):
    try:
        cursor = conexion.connection.cursor()

        sql = "DELETE FROM Rutina WHERE idRutina = %s"
        cursor.execute(sql, (idRutina,))
        conexion.connection.commit()

        return jsonify({'mensaje': 'Rutina eliminada correctamente.'})
    except Exception as e:
        return jsonify({'mensaje': 'Error al eliminar la rutina: ' + str(e)})
#Actualizar datos de usuario
@app.route('/actualizar_datos_usuario/<int:idDocumento>', methods=['PUT'])
def actualizar_datos_usuario(idDocumento):
    try:
        # Obtener los datos del cuerpo de la solicitud en formato JSON
        data = request.json

        # Extraer los datos del JSON
        nuevo_nombre1 = data.get('nombre1', '')
        nuevo_nombre2 = data.get('nombre2', '')
        nuevo_apellido1 = data.get('apellido1', '')
        nuevo_apellido2 = data.get('apellido2', '')
        nuevo_correo_electronico = data.get('correoElectronico', '')

        # Crear un cursor para la base de datos
        cursor = conexion.connection.cursor()

        # Consulta SQL para actualizar los datos del usuario
        sql = """
            UPDATE Usuario
            SET Nombre1 = %s, Nombre2 = %s, Apellido1 = %s, Apellido2 = %s, CorreoElectronico = %s
            WHERE idDocumento = %s
        """

        # Ejecutar la consulta SQL con los nuevos datos del usuario
        cursor.execute(sql, (nuevo_nombre1, nuevo_nombre2, nuevo_apellido1, nuevo_apellido2, nuevo_correo_electronico, idDocumento))

        # Confirmar la actualización en la base de datos
        conexion.connection.commit()

        # Retornar un mensaje de éxito
        return jsonify({'mensaje': 'Datos de usuario actualizados correctamente'}), 200
    except Exception as e:
        # Retornar un mensaje de error en caso de fallo en la actualización
        return jsonify({'error': 'Error al actualizar los datos del usuario: ' + str(e)}), 500

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

