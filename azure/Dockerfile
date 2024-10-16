FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto (incluyendo el script y el .env) al contenedor
COPY . .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir requests python-dotenv

# Definir el comando por defecto para ejecutar quickstart.py
CMD ["python", "quickstart.py"]
