import os
from logging.config import fileConfig
from app.models import SQLModel  
from alembic import context
from sqlalchemy import engine_from_config, pool

# entramos en alembic.ini para saber donde guardar las migraciones
 ## y tener loggings por si alguna migracion falla 
 
config = context.config
fileConfig(config.config_file_name) #para almacenar los loggings

# fijamos que alembic se fije en metadatos y detecta cambios en esquema y que haga la migracion
## y luego se actualiza el modelo en la app

target_metadata = SQLModel.metadata

# Función para obtener la URL de la base de datos a partir de las variables de entorno.
def get_url():
    # Obtenemos el usuario, contraseña, servidor, puerto y nombre de la base de datos de las variables de entorno.
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "")
    server = os.getenv("POSTGRES_SERVER", "db")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "app")
    
    # Devolvemos la URL completa de la base de datos en formato PostgreSQL.
    return f"postgresql+psycopg://{user}:{password}@{server}:{port}/{db}"

# Función para ejecutar las migraciones en modo offline.
def run_migrations_offline():
    """
    Ejecutar las migraciones en modo 'offline'.
    En este modo, no necesitamos una conexión activa a la base de datos.
    Se configura el contexto solo con una URL y no se crea un Engine.
    """
    url = get_url()
    
    # Configuramos el contexto con la URL y los metadatos del modelo.
    # También usamos 'literal_binds=True' para que los valores literales se enlacen directamente.
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    # Iniciamos la transacción para ejecutar las migraciones.
    with context.begin_transaction():
        context.run_migrations()

# Función para ejecutar las migraciones en modo online.
def run_migrations_online():
    """
    Ejecutar las migraciones en modo 'online'.
    En este modo, se crea un Engine y se asocia una conexión con el contexto.
    """
    # Obtenemos la configuración del archivo .ini y la URL de la base de datos.
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    # Creamos un Engine usando la configuración obtenida.
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Usamos el Engine para crear una conexión y asociarla al contexto.
    with connectable.connect() as connection:
        # Configuramos el contexto con la conexión activa y los metadatos del modelo.
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        # Iniciamos la transacción para ejecutar las migraciones.
        with context.begin_transaction():
            context.run_migrations()

# Aquí verificamos si Alembic está en modo offline o online.
# Dependiendo del modo, se llama a la función correspondiente.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
