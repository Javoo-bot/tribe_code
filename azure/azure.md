# Historial de Comandos para Azure Machine Learning

A continuación, se presenta el historial de comandos utilizados para establecer la conexión y trabajar con Azure Machine Learning desde la consola:

## 1. Lo primero es iniciar sesion Azure CLI:
```bash
az login
```

## 2. Mostrar los recursos que tengo:
```bash
az group list --output table
```

## 3. Mostrar los workspaces de Azure ML dentro de un grupo de recursos:
```bash
az ml workspace list --resource-group UO250680-rg --output table
```

## 4. Registrar proveedores de recursos necesarios para Azure ML:
```bash
az provider register --namespace Microsoft.MachineLearningServices
az provider register --namespace Microsoft.ContainerInstance
az provider register --namespace Microsoft.Storage
```


## 5. Mostrar el estado de los proveedores de recursos registrados, todo tiene que ser "Registred":
```bash
az provider show --namespace Microsoft.MachineLearningServices --query "registrationState"
az provider show --namespace Microsoft.ContainerInstance --query "registrationState"
az provider show --namespace Microsoft.Storage --query "registrationState"
```

## 6a. Crear los archivos .yml para configurar el endpoint:

```bash
$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineEndpoint.schema.json
name: my-endpoint
auth_mode: key
```

Creamos un fichero deployment.yml: aqui se establece el modelo, los recursos y el entorno

```bash
$schema: https://azuremlschemas.azureedge.net/latest/managedOnlineDeployment.schema.json
name: my-endpoint
auth_mode: key
model:
  uri: azureml://registries/azureml/models/TuModelo/versions/1
environment: azureml:my-environment:1
code_configuration:
  code:
    path: ./src  # Ruta a tu código de inferencia
  scoring_script: score.py  # Script que hará las predicciones
instance_type: Standard_DS2_v2
instance_count: 1
```

## 6b. Intento de creación de un endpoint en tiempo real (con error):
```bash
az ml online-endpoint create --name my-endpoint --file endpoint.yml --resource-group UO250680-rg --workspace-name Tribe
```

#pero me da error 

## 7. Ver roles asignados a una cuenta específica en el grupo de recursos:
```bash
az role assignment list --assignee uo250680@uniovi.es --resource-group UO250680-rg
```
Si me da owner entoncer el problema esta en otro lado...

Probar el proximo dia si el problema esta en la región donde estás desplegando el modelo es compatible con el tipo de modelo que estás utilizando...
