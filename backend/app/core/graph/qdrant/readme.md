# Basic Qdrant Documentation

Este documento describe la configuración y el uso basico Qdrant como base de datos vectorial en el proyecto. A continuación se detallan los distintos archivos y componentes donde aparece Qdrant y cómo se gestiona.

## Índice

1. [Configuración de Qdrant](#configuracion-de-qdrant)
    - [Settings-local.yaml](#settings-local-yaml)
    - [Settings.yaml](#settings-yaml)
    - [Settings.py](#settings-py)
2. [Componentes de Qdrant](#componentes-de-qdrant)
    - [Vector Store Component](#vector-store-component)
    - [Utils.py](#utils-py)
    - [Auto_close_qdrant.py](#auto-close-qdrant-py)
3. [Ejemplos de Código](#ejemplos-de-codigo)
    - [Inicialización del cliente Qdrant](#inicializacion-del-cliente-qdrant)
    - [Recuperador de índices](#recuperador-de-indices)

---

## Configuración de Qdrant <a name="configuracion-de-qdrant"></a>

### Settings-local.yaml

- **Definición de la Base Vectorial para el Modelo Ollama**: Este archivo define la configuración local para Qdrant. Permite modificar parámetros de configuración, pero no incluye detalles sobre la conexión a Qdrant.
- **Configuración Local**:
  - Almacenamiento de Qdrant en un archivo local.

### Settings.yaml

- **Configuración Global del Sistema**: Incluye configuraciones generales del vector store.
  - **Vector Store**: Define la base de datos utilizada para almacenar los vectores.
  - **RAG** (Retrieval-Augmented Generation): Especifica el vector a usar, el modelo para el análisis y el número de coincidencias.

### Settings.py

- **Configuración del Vector Store con Pydantic**: Configuración de Qdrant a través de Pydantic.

```python
class QdrantSettings(BaseModel):
    location: str | None = Field(
        None,
        description=(
            "If `:memory:` - use in-memory Qdrant instance.\n"
            "If `str` - use it as a `url` parameter."
        )
    )
    url: str | None = Field(
        None,
        description=(
            "Either host or str of 'Optional[scheme], host, Optional[port], Optional[prefix]'."
        ),
    )
    port: int | None = Field(6333, description="Port of the REST API interface.")
    grpc_port: int | None = Field(6334, description="Port of the gRPC interface.")
    prefer_grpc: bool | None = Field(
        False,
        description="If `true` - use gRPC interface whenever possible in custom methods.",
    )
    https: bool | None = Field(
        None,
        description="If `true` - use HTTPS(SSL) protocol.",
    )
    api_key: str | None = Field(
        None,
        description="API key for authentication in Qdrant Cloud.",
    )
    prefix: str | None = Field(
        None,
        description=(
            "Prefix to add to the REST URL path."
            "Example: `service/v1` will result in "
            "'http://localhost:6333/service/v1/{qdrant-endpoint}' for REST API."
        ),
    )
    timeout: float | None = Field(
        None,
        description="Timeout for REST and gRPC API requests.",
    )
    host: str | None = Field(
        None,
        description="Host name of Qdrant service. If url and host are None, set to 'localhost'.",
    )
    path: str | None = Field(None, description="Persistence path for QdrantLocal.")
    force_disable_check_same_thread: bool | None = Field(
        True,
        description=(
            "For QdrantLocal, force disable check_same_thread. Default: `True`"
            "Only use this if you can guarantee that you can resolve the thread safety outside QdrantClient."
        ),
    )
```

## Componentes de Qdrant <a name="componentes-de-qdrant"></a>

### Vector Store Component <a name="vector-store-component"></a>

- **Vector Store Component**: Define Qdrant como la base vectorial entre otras opciones disponibles.

```python
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

client = QdrantClient()

self.vector_store = typing.cast(
    BasePydanticVectorStore,
    QdrantVectorStore(
        client=client,
        collection_name="col1"
    )
)
```

- **Retriever**:

```python
def get_retriever(
        self,
        index: VectorStoreIndex,
        context_filter: ContextFilter | None = None, # en Qdrant no usamos filtros
        similarity_top_k: int = 2) -> VectorIndexRetriever:
    
    return VectorIndexRetriever(
        index=index,
        similarity_top_k=similarity_top_k,
        doc_ids=context_filter.docs_ids if context_filter else None,
        filters=(_doc_id_metadata_filter(context_filter))
    )

def close(self) -> None:
    if hasattr(self.vector_store.client, "close"):
        self.vector_store.client.close()
```

### Utils.py <a name="utils-py"></a>

- **Inicialización de la Base de Datos Qdrant**: Inicializa la base de datos Qdrant y la pone en funcionamiento.

```python
class Qdrant:
    COLLECTION = ("col1")

    def __init__(self) -> None:
        from qdrant_client import QdrantClient  
        self.client = QdrantClient(**settings().qdrant.model_dump(exclude_none=True))

    def wipe(self, store_type: str) -> None:
        assert store_type == "vectorstore"
        self.client.delete_collection(self.COLLECTION)
        print("Collection dropped successfully.")

    def stats(self, store_type: str) -> None:
        print(f"Storage for Qdrant {store_type}.")
        collection_data = self.client.get_collection(self.COLLECTION)
        if collection_data:
            print(f"\tPoints:        {collection_data.points_count:,}")
            print(f"\tVectors:       {collection_data.vectors_count:,}")
            print(f"\tIndex Vectors: {collection_data.indexed_vectors_count:,}")
            return
```

### Auto_close_qdrant.py <a name="auto-close-qdrant-py"></a>

- **Cierre Automático de la Base de Datos**: Cierra la base de datos Qdrant después de cada prueba para asegurar un correcto uso de recursos.

```python
def _auto_close_vector_store_client(injector: MockInjector) -> None:
    """Auto close VectorStore client after each test.
    """
    yield
    injector.get(VectorStoreComponent).close()
```

## Ejemplos de Código <a name="ejemplos-de-codigo"></a>

### Inicialización del Cliente Qdrant <a name="inicializacion-del-cliente-qdrant"></a>

```python
from qdrant_client import QdrantClient

client = QdrantClient()
```

### Recuperador de Índices <a name="recuperador-de-indices"></a>

```python
def get_retriever(
        self,
        index: VectorStoreIndex,
        context_filter: ContextFilter | None = None,
        similarity_top_k: int = 2) -> VectorIndexRetriever:
    
    return VectorIndexRetriever(
        index=index,
        similarity_top_k=similarity_top_k,
        doc_ids=context_filter.docs_ids if context_filter else None,
        filters=(_doc_id_metadata_filter(context_filter))
    )
```


