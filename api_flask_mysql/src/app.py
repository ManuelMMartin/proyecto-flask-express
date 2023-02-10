from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

conexion = MySQL(app)


@app.route('/', methods=['GET'])
def listar_tareas_bd():
    try:
        cursor = conexion.connection.cursor()
        sql = 'SELECT * FROM tasklist'
        cursor.execute(sql)
        datos = cursor.fetchall()
        taskList = []
        for fila in datos:
            task = {
                'numero': fila[0],
                'titulo': fila[1],
                'descripcion': fila[2],
                'prioridad': fila[3],
                'completada': fila[4]
            }
            taskList.append(task)
        return jsonify({'results': taskList, 'mensaje': 'Tareas recuperadas de la BD'})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


def listar_tarea_bd(numero):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT numero, titulo, descripcion, prioridad, completada FROM tasklist WHERE numero = '{0}'".format(
            numero)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            tarea = {
                'numero': datos[0],
                'titulo': datos[1],
                'descripcion': datos[2],
                'prioridad': datos[3],
                'completada': datos[4]
            }
            return tarea
        else:
            return None
    except Exception as ex:
        raise ex


@app.route('/<numero>', methods=['GET'])
def leer_tarea(numero):
    try:
        tarea = listar_tarea_bd(numero)
        if tarea != None:
            return jsonify({'tarea': tarea, 'mensaje': "tarea encontrado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Tarea no encontrado.", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'exito': False})


@app.route('/add', methods=['POST'])
def registrar_tarea():
    print(request.json['numero'])
    try:
        tarea = listar_tarea_bd(request.json['numero'])
        if tarea != None:
            return jsonify({'mensaje': "La tarea con el numero indicado ya existe, no se puede duplicar.", 'exito': False})
        else:
            cursor = conexion.connection.cursor()
            sql = """INSERT INTO tasklist (numero, titulo, descripcion, prioridad, completada) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '0')""".format(request.json['numero'], request.json['titulo'], request.json['descripcion'], request.json['prioridad'],)
            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje': "Agregada la tarea"})
    except Exception as ex:
        raise ex


@app.route('/borrar', methods=['DELETE'])
def eliminar_tarea():
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM tasklist WHERE numero = '{0}'".format(
            request.json['numero'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': 'Tarea borrada'})
    except Exception as ex:
        raise ex


@app.route('/completar', methods=['PUT'])
def completar_tarea():
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE tasklist SET completada ='{0}' WHERE numero = '{1}'".format(
            1, request.json['numero'])
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'mensaje': 'Tarea completada'})
    except Exception as ex:
        raise ex


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
