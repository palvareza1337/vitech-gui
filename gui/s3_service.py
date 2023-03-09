# boto3 es el nombre del awssdk para python
import time
start = time.time()

import boto3
import os

# cargar las variables de entorno desde un archivo .env
from dotenv import load_dotenv
load_dotenv(dotenv_path="gui/.env")

# iniciacion del cliente de aws para s3
# AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY son variables de entorno, 
s3 = boto3.client('s3', aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])

# creacion de la carpeta cache si es que esta no existe
if not os.path.exists("cache"):
    os.mkdir("cache")

# funcion que descarga un archivo de s3 a partir de su nombre
def download_reading(reading_key):
    print("downloading " + reading_key)
    s3.download_file('vitech-staging', reading_key,  os.path.join("cache", reading_key))

# funcion para buscar un archivo en el cache, previo intento de descarga desde s3
def get_reading(reading_key):
    # si existe el archivo en cache, entregar el archivo
    if os.path.exists(os.path.join("cache", reading_key)):
        print("hit")
    # si el archivo no existe en cache, intentar descargarlo desde s3
    else:
        try:
            download_reading(reading_key)
            print("downloaded")
        # en caso de que no se pueda descargar, si no se tienen permisos / no existe el archivo / otra razon de fuerza mayor
        # imprimir el error en pantalla y retornar None
        except:
            print("failed to download")
            return None
    # retornar el path del archivo que se buscaba
    return os.path.join("cache", reading_key)

end = time.time()
print("conected to S3 in " + str(end-start) + " seconds")




# import guard/ tambien es posible utilizar este espacio para probar la libreria sin la necesidad del main por completo
if __name__=="__main__":
    # descarga un archivo desde s3
    get_reading("Z - 18927640307-02-2023 16,37,43.csv")
    # lista los s3 buckets a los cuales la cuenta en especifico tiene acceso
    response = s3.list_buckets()
    print('Existing buckets:')
    for bucket in response['Buckets']:
        print(f'  {bucket["Name"]}')