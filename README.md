# Serverless ETL Pipeline: S3 a DynamoDB

## 1. Descripción del Proyecto
Este proyecto automatiza la ingesta de archivos de texto. Detecta archivos subidos a un Data Lake (S3), los procesa para identificar contenido "URGENTE" y registra los metadatos en una base de datos NoSQL (DynamoDB).

## 2. Arquitectura
* **Source:** Amazon S3 (Bucket: `laboratorio-diego...`)
* **Trigger:** S3 Event Notification (PutObject)
* **Compute:** AWS Lambda (Python 3.13 + Boto3)
* **Database:** Amazon DynamoDB (Tabla: `RegistroProcesos`)

## 3. Flujo de Datos
1.  Usuario sube archivo `.txt` a carpeta `entradas/`.
2.  S3 detecta evento y dispara Lambda.
3.  Lambda lee el archivo y busca la palabra clave "URGENTE".
4.  Si es urgente -> Guarda registro en DynamoDB.
5.  Si no es urgente -> Solo procesa el archivo en S3.
