# Historial de Comandos para Azure Machine Learning

A continuación, se presenta el historial de comandos utilizados para establecer la conexión y trabajar con Azure Machine Learning desde la consola:

## 0 . Crear enviroment en estas zonas:
    - East US 2
    - Sweden 

## 1. Lo primero es iniciar sesion Azure CLI:
```bash
az login
```

## 2. Mostrar los recursos que tengo:
```bash
az group list --output table
```

## 2b. Comprobar mi conexion esta unida al area de trabajo:
```bash
az account show
```

## 3. Mostrar los workspaces de Azure ML dentro de un grupo de recursos:
```bash
az ml workspace list --resource-group UO250680-rg --output table
```

## 4. Registrar proveedores (Microsoft):
```bash
az provider register --namespace Microsoft.MachineLearningServices
az provider register --namespace Microsoft.ContainerInstance
az provider register --namespace Microsoft.Storage
```

## 5. Mostrar el estado de los proveedores de recursos, todo tiene que ser "Registred":
```bash
az provider show --namespace Microsoft.MachineLearningServices --query "registrationState"
```
Lo mismo para "Microsoft.ContainerInstance" y "Microsoft.Storage"

## 6a. Crear el script del connection.yml para configurar el endpoint

```bash
name: Phi-3-mini-128k-instruct-connection
type: serverless
endpoint: https://Phi-3-mini-128k-instruct-rsnsn.eastus2.models.azure.com/score
api_key: {api_key}
```
El error a veces es por el rol de la cuenta, una manera de ver el rol es:

## 7. Ver roles asignados a una cuenta específica en el grupo de recursos:
```bash
az role assignment list --assignee uo250680@uniovi.es --resource-group UO250680-rg
```

## 8. Creacion endopoint (serverless):

  - Se creó un **endpoint sin servidor** en Azure Machine Learning, llamado    `Phi-3-mini-128k-instruct`.

  - Se obtuvieron los detalles del endpoint, incluyendo la URL del endpoint y la clave API,   que se usarán para la conexión.

  - Script de Python crea el archivo `connection.yml`. Este archivo contiene:
       - Nombre conexion
       - El tipo
       - URL endpoint
       - La API
       - Para probar el modelo de chat usamos el kit de software de Azure

## 9. Error al instalar Azure:

  1. **Creo Dockerfile**: 
   - Defino el archivo `Dockerfile` con la configuración necesaria.

  2. **Construyo la imagen**: 
   - Utilizo el siguiente comando para construir la imagen:
     ```bash
     docker build -t mi_entorno_python .
     ```

  3. **Ejecuto el contenedor**: 
   - Una vez construida la imagen, ejecuto el contenedor con:
     ```bash
     docker run mi_entorno_python
     ```

