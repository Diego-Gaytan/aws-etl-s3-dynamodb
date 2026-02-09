import json
import boto3
import urllib.parse
import os
from datetime import datetime

# --- CONFIGURACIÓN ---
# Definimos las conexiones aquí arriba para no tener que conectar 
# cada vez que se ejecuta la función (es más eficiente).
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('RegistroProcesos')

def lambda_handler(event, context):
    try:
        # 1. OBTENER INFORMACIÓN DEL ARCHIVO
        # Sacamos el nombre del bucket y del archivo que se acaba de subir
        bucket_origen = event['Records'][0]['s3']['bucket']['name']
        
        # Usamos unquote_plus para arreglar los nombres si tienen espacios o caracteres raros
        key_origen = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        print(f"Procesando archivo: {key_origen}")
        
        # 2. LEER EL ARCHIVO
        response = s3.get_object(Bucket=bucket_origen, Key=key_origen)
        contenido = response['Body'].read().decode('utf-8')
        
        # 3. TRANSFORMACIÓN (ETL)
        # Convertimos todo a mayúsculas como regla de negocio
        contenido_mayus = contenido.upper()
        
        # Preparamos el nombre para guardarlo en la carpeta de procesados
        nombre_solo = os.path.basename(key_origen) 
        key_destino = f"procesados/DB_{nombre_solo}" 
        
        # Guardamos el archivo modificado en S3 (esto se hace siempre)
        s3.put_object(Bucket=bucket_origen, Key=key_destino, Body=contenido_mayus)
        
        # 4. FILTRO DE GUARDADO EN BASE DE DATOS
        # Solo guardamos registro en DynamoDB si el archivo es realmente importante ("URGENTE")
        if "URGENTE" in contenido_mayus:
            
            timestamp_actual = str(datetime.now())
            
            tabla.put_item(
                Item={
                    'nombre_archivo': nombre_solo,      # Llave principal
                    'fecha_registro': timestamp_actual, # Fecha para el historial
                    'tamaño_bytes': len(contenido),
                    'estado': 'CRITICO_URGENTE',
                    'ruta_final': key_destino
                }
            )
            print(">> Archivo Urgente: Guardado en base de datos correctamente.")
            
        else:
            print(">> Archivo Normal: No se guarda en base de datos para ahorrar espacio.")
        
        return "Todo salió bien"

    except Exception as e:
        print(f"Error grave: {str(e)}")
        raise e
