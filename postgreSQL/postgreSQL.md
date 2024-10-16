# Documentacion de PostgreSQL

Para conectarnos ponemos los valores las credenciales de postgreSQL en .env 

Luego el docker compose coje los datos de .env

La app usa SQLAlchemy como ORM para conectarse a PostgreSQL.Es decir no hay consultas SQL directas

Las conexiones a la db se abren y cierran con cada consulta porque usamos NullPool.  

Si hay desconexion automatica no hay un mecanismo para reiniciar la app. 

Los modelos de la base de datos estan en models.py.

Usamos Alembic para hacer las migraciones. Si queremos añadir modelos o modificar los existentes editamos carpeta alembic. 

Puedes añadir nuevos modelos o modificar los existentes editando este archivo y luego generando las migraciones necesarias con Alembic.

Queda por mirar que consultas lentas hay en PostgreSQL. Esto se puede hacer con tecnicas como indexación o paginación.

## Estructura general del proyecto

- [x] Configuración de la Conexión a la Base de Datos (config)
- [x] Manejo de la Base de Datos (core/db.py) 
- [x] Estructura de Datos y Tablas (models)
- [x] Migración de Datos (alembic)
- [x] Operaciones basicas en db : CRUD (crud.py)
- [x] Datos Iniciales (initial_data)

- **Config**
   - Creación de un servidor local para desarrollo.
   - Configuración de la conexión del backend a PostgreSQL.
   - Interacción con PostgreSQL usando un ORM (SQLAlchemy) en Python.
   - Almacenamiento seguro de claves y credenciales mediante variables de entorno.

- **Core**
   - Base datos se gestiona usando alembic
   - En alembic se gestiona todo
   - Sino funcionase alembic (puede pasar) habria que: 
       - Definir modelos
       - Conexion base datos (URI): postgresql+psycopg://admin:secret@localhost:5432/mydatabase
       - Verificar existencia tablas
       - Sino existen, crear tablas
       - Agregar datos
       - Copia de seguridad

-**Models**
   - Tiene 8 subsecciones pero con misma estructura 
   - Analizamos estructura de Team que se usa para la gestion de equipos
       - Definimos atributos basicos
       - Clase para crear y luego actualizar equipos
       - Clase Team donde se definen relacion one-to-many, many-to-many y restricciones (parte fundamental)
        ** Muy importante como configuramos las relaciones **
       - Configurar el modelo de salida si hacemos peticion API

-**Alembic**
   - En env configuramos las migraciones, se guardan en version y se actualizan solas en docker. 
   - Maiko: esquema funcionamiento migracion que siguen todas las `versions`
   - Empezemos por .env:
     - Dos modos de funcionamiento: **offline** y **online**.
     - Nos conectamos con `get_url()`a la base de datos
     - Si hay cambios metadatos Alembic hace automaticamente migraciones
     - Usamos variables de entorno para conexion 
       - Modo offline: genera scripts SQL sin conectarse db. Util cuando db no disponible
       - Modo online: hace migraciones tiempo real. Necesita motor SQLAlchemy. 
   
-**Crud**
   - Define operaciones creación, lectura, actualización y eliminación interactua con bd

-**Initial data**
   - Iniciar bd e insertar datos cuando la aplicación comienza.

## Pasos creacion nueva tabla: ampliar memoria del LLM + conocimiento especifico + contexto 

   - Nuevo modelo en models.py : nuevos atributos, relaciones y restricciones
   - Nueva migracion en alembic
   - Revisar el archivo de migración que se va a generar 
   - Aplicar la migración en bd : se hace desde docker 
   - Verificar la creación de la nueva tabla en PostgreSQL

