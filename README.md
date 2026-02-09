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

## 4. Arquitectura del Sistema
```mermaid
graph LR
    User([Usuario]) -- "1. Sube archivo" --> S3[Amazon S3\n(Bucket)]
    S3 -- "2. Dispara Evento" --> Lambda[AWS Lambda\n(Python)]
    Lambda -- "3a. Si es URGENTE" --> DDB[(Amazon DynamoDB)]
    Lambda -- "3b. Si es NORMAL" --> Logs[CloudWatch Logs]
    
    style S3 fill:#E1F5FE,stroke:#01579B
    style Lambda fill:#FFF3E0,stroke:#FF6F00
    style DDB fill:#E8F5E9,stroke:#1B5E20
