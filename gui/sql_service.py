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

# literalmente es un placeholder a un eventual login
def login(username, password):
  id_usuario = 1
  return id_usuario

def buscar_empresa(id_empresa = 17123456):
  cursor.execute(f"SELECT id_empresa, nombre_empresa, nombre_cliente, contacto_cliente FROM empresa WHERE id_empresa={id_empresa}")
  result = cursor.fetchone()
  temp = dict()
  temp["id_empresa"] = result[0]
  temp["nombre_empresa"] = result[1]
  temp["nombre_cliente"] = result[2]
  temp["contacto_cliente"] =  result[3]
  return temp

def buscar_sucursales_por_empresa(id_empresa):
  cursor.execute(f"SELECT id_sucursal, id_empresa, nombre_sucursal, direccion, contacto_sucursal FROM sucursal WHERE id_empresa={id_empresa}")
  results = cursor.fetchall()
  out = []
  for result in results:
    temp = dict()
    temp["id_sucursal"] = result[0]
    temp["id_empresa"] = result[1]
    temp["nombre_sucursal"] = result[2]
    temp["direccion"] = result[3]
    temp["contacto_sucursal"] = result[4]
    out.append(temp)
  return out

def buscar_areas_por_sucursal(id_sucursal):
  cursor.execute(f"SELECT id_area, id_sucursal, numero_maquinas, nombre_area FROM area WHERE id_sucursal='{id_sucursal}'")
  results = cursor.fetchall()
  out = []
  for result in results:
    temp = dict()
    temp["id_area"] = result[0]
    temp["id_sucursal"] = result[1]
    temp["numero_maquinas"] = result[2]
    temp["nombre_area"] = result[3]
    out.append(temp)
  return out

def buscar_maquinas_por_area(id_area):
  cursor.execute(f"SELECT id_maquina, id_area, nombre_maquina, tipo_maquina, modelo, cant_puntos_monitoreo, criticidad FROM maquina WHERE id_area='{id_area}'")
  results = cursor.fetchall()
  out = []
  for result in results:
    temp = dict()
    temp["id_maquina"] = result[0]
    temp["id_area"] = result[1]
    temp["nombre_maquina"] = result[2]
    temp["tipo_maquina"] = result[3]
    temp["modelo"] = result[4]
    temp["cant_puntos_monitoreo"] = result[5]
    temp["criticidad"] = result[6]
    out.append(temp)
  return out

def buscar_maquina_por_id(id_maquina):
  cursor.execute(f"SELECT id_maquina, id_area, nombre_maquina, tipo_maquina, modelo, cant_puntos_monitoreo, criticidad FROM maquina WHERE id_maquina='{id_maquina}'")
  result = cursor.fetchone()
  temp = dict()
  temp["id_maquina"] = result[0]
  temp["id_area"] = result[1]
  temp["nombre_maquina"] = result[2]
  temp["tipo_maquina"] = result[3]
  temp["modelo"] = result[4]
  temp["cant_puntos_monitoreo"] = result[5]
  temp["criticidad"] = result[6]
  return temp

def buscar_zona_analisis_por_maquina(id_maquina):
  cursor.execute(f"SELECT id_zona_analisis, id_maquina, nombre_zona, estado_salud, cant_sensores FROM zona_analisis WHERE id_maquina='{id_maquina}'")
  results = cursor.fetchall()
  out = []
  for result in results:
    temp = dict()
    temp["id_zona_analisis"] = result[0]
    temp["id_maquina"] = result[1]
    temp["nombre_zona"] = result[2]
    temp["estado_salud"] = result[3]
    temp["cant_sensores"] = result[4]
    out.append(temp)
  return out

def buscar_zona_analisis_por_id(id_zona):
  cursor.execute(f"SELECT id_zona_analisis, id_maquina, nombre_zona, estado_salud, cant_sensores FROM zona_analisis WHERE id_zona_analisis='{id_zona}'")
  result = cursor.fetchone()
  temp = dict()
  temp["id_zona_analisis"] = result[0]
  temp["id_maquina"] = result[1]
  temp["nombre_zona"] = result[2]
  temp["estado_salud"] = result[3]
  temp["cant_sensores"] = result[4]
  return temp

def buscar_punto_por_zona(zona_analisis):
  cursor.execute(f"SELECT id_punto, id_zona_analisis, nombre_punto, tipo_sensor, codigo_sensor, rpm_min, rpm_max, axiales FROM punto WHERE id_zona_analisis='{zona_analisis}'")
  results = cursor.fetchall()
  out = []
  for result in results:
    temp = dict()
    temp["id_punto"] = result[0]
    temp["id_zona_analisis"] = result[1]
    temp["nombre_punto"] = result[2]
    temp["tipo_sensor"] = result[3]
    temp["codigo_sensor"] = result[4]
    temp["rpm_min"] = result[5]
    temp["rpm_max"] = result[6]
    temp["axiales"] = result[7]
    out.append(temp)
  return out

def buscar_punto_por_id(id_punto):
  cursor.execute(f"SELECT id_punto, id_zona_analisis, nombre_punto, tipo_sensor, codigo_sensor, rpm_min, rpm_max, axiales \
                 FROM punto\
                 WHERE id_punto='{id_punto}'")

  result = cursor.fetchone()
  temp = dict()
  temp["id_punto"] = result[0]
  temp["id_zona_analisis"] = result[1]
  temp["nombre_punto"] = result[2]
  temp["tipo_sensor"] = result[3]
  temp["codigo_sensor"] = result[4]
  temp["rpm_min"] = result[5]
  temp["rpm_max"] = result[6]
  temp["axiales"] = result[7]

  return temp

def buscar_lectura_por_punto(id_punto):
  cursor.execute(f"SELECT codigo_sensor, date_time, id_punto, sample_rate, temperatura, ruta_canal_1, ruta_canal_2, ruta_canal_3 FROM lectura WHERE id_punto={id_punto}")
  results = cursor.fetchall()
  out = []
  for result in results:
    temp = dict()
    temp["codigo_sensor"] = result[0]
    temp["date_time"] = result[1]
    temp["id_punto"] = result[2]
    temp["sample_rate"] = result[3]
    temp["temperatura"] = result[4]
    temp["ruta_canal_1"] = result[5]
    temp["ruta_canal_2"] = result[6]
    temp["ruta_canal_3"] = result[7]
    out.append(temp)
  return out

def ultima_lectura():
  cursor.execute(f"SELECT codigo_sensor, date_time, id_punto, sample_rate, temperatura, ruta_canal_1, ruta_canal_2, ruta_canal_3 FROM lectura WHERE date_time = (SELECT MAX(date_time) from lectura);")
  result = cursor.fetchone()
  temp = dict()
  temp["codigo_sensor"] = result[0]
  temp["date_time"] = result[1]
  temp["id_punto"] = result[2]
  temp["sample_rate"] = result[3]
  temp["temperatura"] = result[4]
  temp["ruta_canal_1"] = result[5]
  temp["ruta_canal_2"] = result[6]
  temp["ruta_canal_3"] = result[7]
  return temp

def get_pestana(filename):
  cursor.execute(f"SELECT lectura.sample_rate, area.nombre_area, maquina.modelo, zona_analisis.nombre_zona, punto.nombre_punto\
                  FROM lectura\
                  INNER JOIN punto ON punto.id_punto=lectura.id_punto\
                  INNER JOIN zona_analisis ON zona_analisis.id_zona_analisis=punto.id_zona_analisis\
                  INNER JOIN maquina ON maquina.id_maquina=zona_analisis.id_maquina\
                  INNER JOIN area ON area.id_area=maquina.id_area\
                  WHERE ruta_canal_1 = '{filename}' OR ruta_canal_2 = '{filename}' OR ruta_canal_3 = '{filename}';")
                  
  result = cursor.fetchone()
  temp = dict()
  temp["sample_rate"] = result[0]
  temp["nom_area"] = result[1]
  temp["modelo"] = result[2]
  temp["nombre_zona"] = result[3]
  temp["nombre_punto"] = result[4]
  return result



def agregar_rodamiento(id_rodamiento, id_punto, altura, rigidez, diametro_externo, masa, marca, fabricante, modelo):
  cursor.execute(f"INSERT INTO `rodamiento` (`id_rodamiento`, `id_punto`, `altura`, `rigidez`, `diametro_externo`, `masa`, `marca`, `fabricante`, `modelo`)\
                  VALUES ('{id_rodamiento}', '{id_punto}', '{altura}', '{rigidez}', '{diametro_externo}', '{masa}', '{marca}', '{fabricante}', '{modelo}')")
  db.commit()
  cursor.execute(f"SELECT id_rodamiento FROM rodamiento ORDER BY id_rodamiento DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]



def agregar_rotores(id_rotores, id_punto, largo, diametro, masa, rigidez, fabricante, modelo, marca):
  cursor.execute(f"INSERT INTO `rotor` (`id_rotor`, `id_punto`, `largo`, `diametro`, `masa`, `rigidez`, `fabricante`, `modelo`, `marca`)\
                   VALUES ('{id_rotores}', '{id_punto}', '{largo}', '{diametro}', '{masa}', '{rigidez}', '{fabricante}', '{modelo}', '{marca}')")
  db.commit()
  cursor.execute(f"SELECT id_rotor FROM rotor ORDER BY id_rotor DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]


def agregar_engrane(id_engrane, id_punto, diametro_total, manzana_diametro, hueco_estandar_diametro, numero_dientes, grosor_total_pinon, largo_manzana_solo, rigidez, masa, tipo, marca, fabricante, modelo):
  cursor.execute(f"INSERT INTO `engrane` (`id_engrane`, `id_punto`, `diametro_total`, `manzana_diametro`, `hueco_estandar_diametro`, `numero_dientes`, `grosor_total_pinon`, `largo_manzana_solo`, `rigidez`, `masa`, `tipo`, `marca`, `fabricante`, `modelo`)\
                   VALUES ('{id_engrane}', '{id_punto}', '{diametro_total}', '{manzana_diametro}', '{hueco_estandar_diametro}', '{numero_dientes}', '{grosor_total_pinon}', '{largo_manzana_solo}', '{rigidez}', '{masa}', '{tipo}', '{marca}', '{fabricante}', '{modelo}')")
  db.commit()
  cursor.execute(f"SELECT id_engrane FROM engrane ORDER BY id_engrane DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]



def agregar_eje(id_eje, id_punto, largo, diametro, masa, rigidez, fabricante, marca, modelo):
  cursor.execute(f"INSERT INTO `eje` (`id_eje`, `id_punto`, `largo`, `diametro`, `masa`, `rigidez`, `fabricante`, `marca`, `modelo`)\
                   VALUES ('{id_eje}', '{id_punto}', '{largo}', '{diametro}', '{masa}', '{rigidez}', '{fabricante}', '{marca}', '{modelo}')")
  db.commit()
  cursor.execute(f"SELECT id_eje FROM eje ORDER BY id_eje DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]



def agregar_punto(id_zona_analisis, nombre_punto, tipo_sensor, codigo_sensor, rpm_min, rpm_max, axiales):
  cursor.execute(f"INSERT INTO punto (`id_punto`, `id_zona_analisis`, `nombre_punto`, `tipo_sensor`, `codigo_sensor`, `rpm_min`, `rpm_max`, `Axiales`)\
                  VALUES (NULL, '{id_zona_analisis}', '{nombre_punto}', '{tipo_sensor}', '{codigo_sensor}', '{rpm_min}', '{rpm_max}', '{axiales}')")
  db.commit()
  cursor.execute(f"SELECT id_punto FROM punto ORDER BY id_punto DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]



def agregar_maquina(id_area, tipo_maquina, modelo, cant_puntos_monitoreo, criticidad, nombre_maquina):
  #TODO:
  cursor.execute(f"INSERT INTO maquina(`id_maquina`, `id_area`, `nombre_maquina`, `tipo_maquina`, `modelo`, `cant_puntos_monitoreo`, `criticidad`)\
                  VALUES(NULL, '{id_area}', '{nombre_maquina}', '{tipo_maquina}','{modelo}', '{cant_puntos_monitoreo}', '{criticidad}')")
  db.commit()
  cursor.execute(f"SELECT id_maquina FROM maquina ORDER BY id_maquina DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]

def agregar_area(nombre_area, id_sucursal):
  print(f"INSERT INTO area VALUES(NULL, '{id_sucursal}', '{nombre_area}', NULL)")
  cursor.execute(f"INSERT INTO area(`id_area`, `id_sucursal`, `numero_maquinas`, `nombre_area`) VALUES(NULL, '{id_sucursal}', 1,'{nombre_area}')")
  #cursor.execute(f"SELECT area VALUES(NULL, '{id_sucursal}', '{nombre_area}', NULL)")
  db.commit()
  cursor.execute(f"SELECT id_area FROM area ORDER BY id_area DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]

def agregar_zona(nombre_zona, id_maquina, estado_salud, cant_sensores):
  cursor.execute(f"INSERT INTO zona_analisis(`id_zona_analisis`, `id_maquina`, `nombre_zona`, `estado_salud`, `cant_sensores`)\
                  VALUES(NULL, '{id_maquina}', '{nombre_zona}', '{estado_salud}', {cant_sensores})")
  db.commit()
  cursor.execute(f"SELECT id_zona_analisis FROM zona_analisis ORDER BY id_zona_analisis DESC LIMIT 1")
  result = cursor.fetchone()
  return result[0]  



end = time.time()

print("conected to db in " + str(end-start) + " seconds")

if __name__ == '__main__' : 
  print(get_pestana("Z - 1892763021-18-2023 7,19,16 PM.csv"))