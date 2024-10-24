# Qdrant & RAG Experimentation: The Road to Building Intelligent Client Data Retrieval

## Overview
In this journey, we explored how **Anthropic** built its RAG (Retrieval-Augmented Generation) system and how we could leverage **Qdrant** to implement a similar approach. By simplifying the process and focusing on hosted databases, we set out to improve how we handle customer data with modern embedding techniques.

## Components and Concepts Explored

### 1. Anthropic RAG System
- **Vector Store**: Anthropic's implementation predominantly uses **Pinecone** as a vector store, but we explored the possibility of using **Qdrant** instead.
- **Requirements**: To interact effectively with Claude and manage data retrieval, Anthropic utilizes:
  - **Anthropic API**: For Claude's interactions.
  - **VoyageAI**: For database management.
  - **pandas, numpy, matplotlib, scikit-learn**: To process, analyze, and visualize data.
- **Local vs Hosted Vector Database**: In Anthropic's system, we evaluated a **local vector DB** (like in the `VectorDB` class example) but opted for a **hosted** solution using Docker-hosted Qdrant.

### 2. RAG Workflow Basics
- **Data Preparation**: Loaded documents as a base of knowledge—formed by combining all relevant text chunks.
- **Database Initiation**: Set up a vector database.
- **Question Structuring**: Defined how the queries are formulated and processed.

### 3. Evaluation Techniques
- Metrics used to evaluate RAG performance:
  - **Precision**
  - **Recall**
  - **F1 Score**
  - **MRR (Mean Reciprocal Rank)**
  - **End-to-End Accuracy**
- **Optimization**: Considered adding summaries to each chunk for better accuracy. Implemented a methodology to add embedding that integrates headings, summaries, and original content.

## Inserting Client Data into Qdrant
To explore the potential of **Qdrant** for RAG, we started with the goal of embedding and storing structured client information using metadata. For example:
- **Text**: "Calle Falsa 123, 28000 Madrid, España"
- **Metadata**: `{ "tipo": "direccion_cliente", "cliente": "Apple" }`

This allows better retrieval and relevance through embedding, where each data point is tagged with additional metadata to assist in context-specific searches.

## Steps Taken During Development
### Step-by-Step Process
1. **Pull Qdrant Docker Image**
   - We used Qdrant’s Docker image to quickly set up the hosted instance:
   ```sh
   docker pull qdrant/qdrant
   ```
   - Run the container:
   ```sh
   docker run -d --name qdrant -p 6333:6333 qdrant/qdrant
   ```

2. **Create Dockerfile for Testing**
   - Developed a **Dockerfile** to create an image that runs a **test script** (`test_qdrant.py`). This script was designed to connect to Qdrant and test the functionality of storing and retrieving embeddings.
   - Build the Docker image:
   ```sh
   docker build -t my_qdrant_script .
   ```

3. **Running the Container**
   - Execute the container using network settings that ensure connection to the Qdrant instance:
   ```sh
   docker run --network="host" my_qdrant_script
   ```

4. **Interactive Queries to Qdrant**
   - To make queries without repeatedly building the Docker image, we used:
   ```sh
   docker run -it --network="host" my_test2 /bin/bash
   ```
   - This allowed us to directly use Python within the container to interact with Qdrant and run queries.

5. **Verifying Data in Qdrant**
   - We executed the following Python snippet to check if our data was inserted correctly:
   ```python
   from qdrant_client import QdrantClient

   # Connect to Qdrant
   client = QdrantClient(host="localhost", port=6333)
   collection_name = "client_data"

   point_id = 1
   point_data = client.retrieve(collection_name=collection_name, ids=[point_id])
   print(f"Datos del punto con ID {point_id}: {point_data}")
   ```
   - Result:
     ```
Datos del punto con ID 1: [Record(id=1, payload={'tipo': 'nombre_empresa_cliente', 'cliente': 'Apple'}, vector=None, shard_key=None, order_value=None)]
     ```
   - **Issue**: We realized that no embeddings were being stored. We needed to incorporate proper embeddings to maximize the effectiveness of our Qdrant database.

## Key Learning: Importance of Using Embeddings
Initially, the data in Qdrant had **no embeddings** (`vector=None`). Without embeddings, Qdrant essentially behaves like a traditional **relational database**—missing the crucial advantage of searching through vector similarities. We corrected this by generating small embeddings to test and evaluate the workflow.

### Simplified Embeddings Test
- We created small, simple embeddings (of size **3**) for testing.
- This allowed us to reduce resource consumption while confirming the end-to-end process of embedding creation, storage, and retrieval.

Conclusion and Future Improvements

Today’s session helped us set the foundation for using Qdrant effectively in a RAG setup by testing the basics of embedding creation, data insertion, and retrieval. Moving forward, we can:

Incorporate more enrich each data chunk to further improve the model's ability to answer complex queries.

---
If you have questions or want to discuss next steps, feel free to reach out. The next logical step would be to expand our dataset and improve embeddings quality to leverage Qdrant's full potential!

