"""RAG: Sam's knowledge library.

Stores reference material in a ChromaDB vector database and retrieves
the most relevant pieces by semantic similarity. A distance threshold
rejects loose matches -- no context is better than wrong context.
"""

import os

import chromadb
from sentence_transformers import SentenceTransformer

# Initialize the embedding model and database
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=os.getenv("CHROMADB_PATH", "./chromadb"))
collection = client.get_or_create_collection("companion_knowledge")

def store(text, source="unknown"):
    """Store a piece of knowledge in the vector database."""
    embedding = embedder.encode(text).tolist()
    # Use a hash of the text as the ID to avoid duplicates
    doc_id = str(abs(hash(text)))
    collection.upsert(
        ids=[doc_id],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"source": source}]
    )

def search(query, n_results=1):
    """Find the most relevant knowledge for a given query."""
    count = collection.count()
    if count == 0:
        return ""
    embedding = embedder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=min(n_results, count),
        include=["documents", "metadatas", "distances"]
    )
    if not results["documents"][0]:
        return ""

    # Filter by relevance threshold - reject loose matches
    THRESHOLD = 0.8
    output = []
    for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
        if dist < THRESHOLD:
            output.append(f"[From {meta['source']}]\n{doc}")
        else:
            print(f"[RAG blocked: distance {dist:.2f} above threshold]")

    return "\n\n".join(output)

def count():
    """How many items are stored."""
    return collection.count()
