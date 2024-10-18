# README: Cómo Cargar un Archivo .sql en PostgreSQL Dentro de Docker

Este documento explica paso a paso cómo cargar un archivo `.sql` en una base de datos PostgreSQL que está corriendo dentro de un contenedor Docker. Esto es muy útil para pruebas rápidas y para evitar modificar el backend en cada cambio. Se pueden realizar pruebas iniciales en SQLite y, si todo funciona, luego realizar las migraciones usando Alembic.

## Paso a Paso

### Paso 1: Cargar el Contenedor de 'db'

Primero, asegúrate de cargar solo el contenedor de la base de datos (`db`). Para ello, usa el siguiente comando:

```bash
# Carga solo el contenedor de 'db'
docker-compose up db
```

### Paso 2: Copiar el Archivo `.sql` al Contenedor

Una vez tengas el archivo `.sql` listo (por ejemplo, `mydatabase.sql`), cópialo al contenedor Docker. Asegúrate de conocer el ID o nombre del contenedor.

Ejecuta el siguiente comando:

```bash
docker cp postgreSQL/mydatabase.sql <container_id>:/tmp/mydatabase.sql
```

Reemplaza `<container_id>` con el ID del contenedor PostgreSQL. Puedes obtener el ID ejecutando `docker ps`.

### Paso 3: Entrar al Contenedor Docker

Entra al contenedor Docker para poder interactuar con la base de datos.

```bash
docker exec -it <container_id> /bin/bash
```

### Paso 4: Conectarse a PostgreSQL con `psql`

Una vez dentro del contenedor, conéctate a la base de datos PostgreSQL usando el cliente `psql`.

```bash
psql -U postgres -d app
```

- `-U postgres` indica el usuario (en este caso, `postgres`).
- `-d app` indica la base de datos a la que te quieres conectar (en este caso, `app`).

### Paso 5: Cargar el Archivo `.sql` Dentro de `psql`

Desde la sesión de `psql`, carga el archivo `.sql` que has copiado al contenedor.

```sql
\i /tmp/mydatabase.sql
```

Este comando ejecuta todas las instrucciones contenidas en el archivo `.sql` y las aplica a la base de datos.

### Paso 6: Verificar las Tablas y los Datos

Una vez que se haya ejecutado el archivo, puedes verificar que las tablas y los datos se han añadido correctamente.

- Para listar las tablas creadas:

  ```sql
  \d
  ```

- Para revisar el contenido de una tabla específica, por ejemplo, `template`:

  ```sql
  SELECT * FROM template;
  ```

### Notas Finales

- **Pruebas Rápidas con SQLite**: Puedes probar primero en SQLite y luego portar el `.sql` a PostgreSQL para probar.
- **Migraciones con Alembic**: Si todo funciona correctamente, podrías convertir estos cambios en una migración formal usando Alembic para integrarlos de manera estable en tu proyecto sin necesidad de "hardcodearlo" en el backend.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```bash
$ alembic revision --autogenerate -m "Add column last_name to User model"
```
Con estos pasos, podrás cargar fácilmente archivos `.sql` en tu base de datos PostgreSQL dentro de Docker para realizar pruebas y verificaciones sin complicaciones adicionales.



