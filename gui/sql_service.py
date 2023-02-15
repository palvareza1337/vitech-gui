# libreria para la conexion a la base de datos mysql
import time
start = time.time()

import mysql.connector
import os
# libreria dotenv, la cual permite cargar variables de entorno desde un archivo .env, util para el cargar contraseñas y datos privaddos sin subirlos al repositorio
from dotenv import load_dotenv

load_dotenv(dotenv_path="gui/.env")


db = mysql.connector.connect(
  host=os.environ['SQLHOST'],
  user=os.environ['SQLUSER'],
  password=os.environ['SQLPASS'],
  database=os.environ['SQLDB']
)

# el cursor de la base de datos, mantiene las querys cno las respuestas
cursor = db.cursor()

# busqueda de lecturas por id de sensor, 
def buscar_lecturas_por_sensor(id_sensor):
    cursor.execute(f"SELECT * FROM lectura WHERE id_sensor={id_sensor}")
    options = cursor.fetchall()
    return options

def recuperar_lectura_por_id(id_lectura):
    cursor.execute(f"SELECT * FROM lectura WHERE id_lectura={id_lectura}")
    result = cursor.fetchone()
    return result

# literalmente es un placeholder a un eventual login
def login(username, password):
  id_usuario = 1
  return id_usuario

def buscar_empresa(id_empresa = 17123456):
  cursor.execute(f"SELECT * FROM empresa WHERE id_empresa={id_empresa}")
  result = cursor.fetchone()
  return result

def buscar_sucursales_por_empresa(id_empresa):
  cursor.execute(f"SELECT * FROM sucursal WHERE id_empresa={id_empresa}")
  result = cursor.fetchall()
  return result

def buscar_areas_por_sucursal(id_sucursal):
  cursor.execute(f"SELECT * FROM area WHERE id_sucursal={id_sucursal}")
  result = cursor.fetchall()
  return result

def buscar_maquinas_por_area(id_area):
  cursor.execute(f"SELECT * FROM maquina WHERE id_area='{id_area}'")
  result = cursor.fetchall()
  return result

def buscar_zona_analisis_por_maquina(id_maquina):
  cursor.execute(f"SELECT * FROM zona_analisis WHERE id_maquina='{id_maquina}'")
  result = cursor.fetchall()
  return result

def buscar_sensor_por_zona(zona_analisis):
  cursor.execute(f"SELECT * FROM sensor WHERE id_zona_analisis='{zona_analisis}'")
  result = cursor.fetchall()
  return result

def buscar_lectura_por_sensor(id_sensor):
  cursor.execute(f"SELECT * FROM lectura WHERE id_sensor={id_sensor}")
  result = cursor.fetchall()
  return result

def ultima_lectura():
  cursor.execute(f"SELECT * FROM lectura WHERE date_time = (SELECT MAX(date_time) from lectura);")
  result = cursor.fetchone()
  return result# recover 2 and 4

end = time.time()

print("conected to db in " + str(end-start) + " seconds")