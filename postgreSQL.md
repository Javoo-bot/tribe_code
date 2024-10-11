# Dudas PostgreSQL

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

- Configuración de la Conexión a la Base de Datos (config)
- Información de la Conexión a la Base de Datos (user)
- Manejo de la Base de Datos (core/db.py)
- Estructura de Datos y Tablas (models)
- Migración de Datos (alembic)
- Operaciones CRUD (crud.py)
- Datos Iniciales (initial_data)
- Tareas Menores de Datos (tasks)

