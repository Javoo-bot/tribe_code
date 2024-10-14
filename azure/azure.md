# Historial de Comandos para Azure Machine Learning

A continuación, se presenta el historial de comandos utilizados para establecer la conexión y trabajar con Azure Machine Learning desde la consola:

## 1. Inicio de sesión en Azure CLI:
```bash
az login
```

## 2. Mostrar los grupos de recursos disponibles:
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


## 5. Mostrar el estado de los proveedores de recursos registrados:
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
Creamos un fichero deplyment.yml: aqui se establece el modelo, los recursos y el entorno

## 6b. Intento de creación de un endpoint en tiempo real (con error):
```bash
az ml online-endpoint create --name my-endpoint --file endpoint.yml --resource-group UO250680-rg --workspace-name Tribe
```

## 7. Comando para eliminar un endpoint existente (por problemas previos):
```bash
az ml online-endpoint delete --name my-endpoint --resource-group UO250680-rg --workspace-name Tribe --yes
```

## 8. Intento de actualización del endpoint (con error):
```bash
az ml online-endpoint update --name my-endpoint --file endpoint.yml --resource-group UO250680-rg --workspace-name Tribe
```

## 9. Ver roles asignados a una cuenta específica en el grupo de recursos:
```bash
az role assignment list --assignee uo250680@uniovi.es --resource-group UO250680-rg
```

## 10. Asignar rol "Owner" a tu cuenta en el grupo de recursos:
```bash
az role assignment create --assignee uo250680@uniovi.es --role "Owner" --scope /subscriptions/67067181-ef52-4533-b974-a6ad9c1273fd/resourceGroups/UO250680-rg
```

## 11. Intento de creación de un endpoint "serverless" con configuración modificada:
```bash
az ml online-endpoint create --name my-serverless-endpoint --file endpoint.yml --resource-group UO250680-rg --workspace-name Tribe
```

## 12. Mostrar el estado de la suscripción activa:
```bash
az account show
```


