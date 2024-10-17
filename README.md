# Proyecto de Gestión de Plantillas y Análisis de Documentos

## 📄 Descripción del Proyecto

Este proyecto tiene como objetivo investigar si es posible un sistema eficiente para gestionar plantillas y analizar documentos que contienen tanto texto como imágenes. El flujo de trabajo está diseñado para analizar si fuese posible extraer, almacenar y utilizar información relevante de los documentos para generar documentos personalizados según las necesidades del cliente.

## 🚀 Flujo de Trabajo

### 1. Selección y Preparación de Plantillas

- [x] **Identificar y seleccionar las plantillas necesarias para el proyecto.**
- [x] Crear **plantillas mockeadas** debido a la complejidad y longitud de las originales.

### 1b. Configuración de la Base de Datos PostgreSQL

- [x] **Comprender el esquema de cargas en la aplicación con PostgreSQL.**
  - [x] Configurar la base de datos PostgreSQL (escribir documentación en Markdown).
  - [x] Analizar la configuración en `config/core/alembic`.
    - [x] Mirar definicion enviroment 
    - [x] Ver migraciones
  - [x] Examinar los modelos en `backend/app`.

### 1c. Configuración de la Aplicación

- [x] **Estudiar el funcionamiento de los endpoints de Azure.**
  - [x] Seguir el **Quickstart de Azure** para familiarizarse con los servicios.
  - [x] Integrar con **Azure Machine Learning Studio**.
  - [x] Probar el modelo mediante un script para verificar su correcto funcionamiento.
    
### 2. Configuración y Gestión de Plantillas con Información de Clientes

#### 2a. Base de Datos

- [x] **Elegir una base de datos adecuada**: Se ha seleccionado PostgreSQL para gestionar la información de plantillas y clientes.
- [x] Crear una tabla para almacenar las plantillas.
- [x] Crear una tabla para almacenar la información de los clientes.
- [x] Hacer pruebas con SQLite:

   - [x] Definir las consultas SQL para crear las tablas `Template` y `Client`.
   - [x] Guardar las consultas en un archivo `schema.sql`.
   - [x] Ejecutar el archivo SQL en una base de datos SQLite para crear las tablas.
   - [x] Insertar datos de prueba en las tablas `Template` y `Client`.
   - [x] Levantar solo el contenedor de PostgreSQL: `docker-compose -f docker-compose.yml -f docker-compose.local.yml up db adminer`
   - [x] **Conectar directamente a PostgreSQL desde VS Code o psql**
   - [x] **Verificar que el contenedor de PostgreSQL está corriendo**
   - [x] **Conectar desde VS Code usando la extensión de PostgreSQL**
   - [x] **Configurar Alembic para conectarse a PostgreSQL**
   - [x] **Documentar como sería migración con Alembic**

**Separación de preocupaciones**: Al separar la gestión de la base de datos de la lógica del backend, garantizamos que la infraestructura de la base de datos se mantenga estable 

**Facilidad para migrar entre entornos**

#### 2b. Plantillas

- [] **Seleccionar el formato de las plantillas**: Se utilizarán archivos en formato **JSON** por su flexibilidad y facilidad para ser parseados.
- [ ] Definir los **marcadores de posición** que serán reemplazados con los datos de los clientes en cada plantilla.

#### 2c. Información del Cliente

- [x] **Determinar cómo se recopilará la información del cliente**: Se utilizará un formulario web para recoger los datos.
- [ ] Implementar la funcionalidad para almacenar los datos del cliente de forma segura en la base de datos.

#### 2d. Módulo de Procesamiento de Formularios

- [ ] Crear un módulo que recupere la plantilla correcta desde la base de datos.
- [ ] Programar la sustitución de los **marcadores de posición** con los datos del cliente.
- [ ] Guardar las plantillas completadas para su posterior uso.

#### 2e. Motor de Plantillas

- [x] **Seleccionar un motor de plantillas**: Se ha decidido usar **Jinja2** en Python para mejorar la eficiencia.
- [ ] Implementar el uso de **Jinja2** en el módulo de procesamiento de formularios.


### 4. Subir Documentos desde PostgreSQL a Qdrant

### 5. Mejorar la Función del Retrieval

### 6. Rellenar Plantilla

## 🛠️ Guía de Implementación

## Crear las Plantillas

### Mejorar la Función del Retrieval

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas participar en este proyecto, por favor, sigue estos pasos:

1. **Fork** el repositorio.
2. **Crea una rama** (`git checkout -b feature/nueva-característica`).
3. **Realiza tus cambios** y **commitea** (`git commit -am 'Añadir nueva característica'`).
4. **Push** a la rama (`git push origin feature/nueva-característica`).
5. **Abre un Pull Request**.

## 📬 Contacto

Para cualquier consulta o sugerencia, puedes contactarme a través de:

- **Correo Electrónico**: [uo250680@uniovi.es]

---

¡Gracias por tu interés en este proyecto!

