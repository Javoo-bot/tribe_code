FROM python:3.12-slim

WORKDIR /app

# Copiar el código (incluido test.py)
COPY . .

# Instalar las dependencias, incluido azure-ai-inference
RUN pip install azure-ai-inference azure-core python-dotenv

# Definir el comando por defecto para ejecutar test.py
CMD ["python", "test.py"]
