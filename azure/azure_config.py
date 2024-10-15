import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la clave de API desde las variables de entorno
api_key = os.getenv("AZURE_API_KEY")

if api_key is None:
    raise ValueError("La clave API no se ha encontrado en las variables de entorno.")

# Crear el archivo connection.yml
with open("connection.yml", "w") as file:
    file.write(f"""
name: Phi-3-mini-128k-instruct-connection
type: serverless
endpoint: https://Phi-3-mini-128k-instruct-rsnsn.eastus2.models.azure.com/score
api_key: {api_key}
    """)

print("Archivo connection.yml generado correctamente.")

