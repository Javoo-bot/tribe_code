# ================================
# Consultas básicas para verificar los datos almacenados
# ================================

# 1. Verificar el número de puntos almacenados en la colección
response = client.count(collection_name=collection_name)
print(f"Número total de puntos en la colección '{collection_name}': {response.count}")

# 2. Realizar una búsqueda de los 3 puntos más similares a un vector de ejemplo
query_vector = generate_embedding("Ciberseguridad en Apple")  # Generar un embedding para la consulta
similar_points = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=3
)
print(f"Los 3 puntos más similares: {similar_points}")

# 3. Buscar puntos con un filtro específico en el payload (ej. cliente = 'Apple')
from qdrant_client.models import Filter, FieldCondition, MatchValue

query_filter = Filter(
    must=[
        FieldCondition(
            key="cliente",
            match=MatchValue(value="Apple")
        )
    ]
)
filtered_points = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=query_filter,
    limit=5
)
print(f"Puntos filtrados con cliente='Apple': {filtered_points}")

# 4. Listar todas las colecciones disponibles en Qdrant
total_collections = client.get_collections()
print(f"Colecciones disponibles: {[collection.name for collection in total_collections.collections]}")


