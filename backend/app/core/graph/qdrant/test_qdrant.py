from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import numpy as np

# Generar embeddings simples y pequeños
# Para esta prueba, generaremos embeddings pequeños de tamaño 3 utilizando valores aleatorios
def generate_simple_embedding(text):
    # Generar un vector pequeño de tamaño 3 con valores aleatorios para simular embeddings
    return np.random.rand(100).tolist()

# Cargar los datos del archivo JSON
import json 

with open('data.json', 'r') as file:
    data = json.load(file)

# Crear una instancia del cliente de Qdrant
client = QdrantClient(host="localhost", port=6333)

# Crear una colección en Qdrant si no existe
collection_name = "client_data"
if not client.collection_exists(collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3, distance=Distance.COSINE),  # Ajusta el tamaño a 3 para los embeddings pequeños
    )

# Insertar los datos en la colección
for item in data:
    vector = generate_simple_embedding(item["text"])  # Generar un embedding pequeño y simple
    point = PointStruct(
        id=item["id"],
        vector=vector,
        payload=item["metadata"],
    )
    client.upsert(collection_name=collection_name, points=[point])

print("Datos insertados correctamente en Qdrant con embeddings pequeños.")


# ================================
# Función para recuperar documentos relevantes de Qdrant
# ================================

def get_relevant_documents(query: str, collection_name: str = collection_name, k: int = 5) -> list:
    """
    Recuperar documentos relevantes de la colección Qdrant usando el texto de la consulta.

    Args:
        query (str): Texto de la consulta.
        collection_name (str): Nombre de la colección donde buscar.
        k (int): Número de documentos relevantes a recuperar.

    Returns:
        list: Lista de documentos relevantes.
    """
    query_vector = generate_simple_embedding(query)  # Generar un embedding pequeño para la consulta
    print(f"Embedding generado correctamente para la consulta: {query}")
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=k
    )
    documents = []
    for result in search_results:
        document = {
            "page_content": result.payload,
            "score": result.score
        }
        documents.append(document)
    return documents

# Ejemplo de uso de la función get_relevant_documents
query = "Ciberseguridad en Apple"
documents = get_relevant_documents(query)
print(f"Documentos relevantes para la consulta '{query}': {documents}")



