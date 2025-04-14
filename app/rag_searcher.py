import faiss
import json
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')


def load_index_and_metadata():
    index = faiss.read_index("app/knowledge_base/rag_index.faiss")
    with open("app/knowledge_base/rag_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)
    return index, metadata


def search_rag(query, agent_level, top_k=3):
    index, metadata = load_index_and_metadata()
    query_embedding = model.encode([query])
    scores, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            chunk = metadata[idx]
            # check if this chunk requires higher clearance
            if "facility x-17" in chunk["content"].lower() and agent_level < 4:
                chunk["content"] = "Access Denied: Classified beyond your clearance level."
            elif "project eclipse" in chunk["content"].lower() and agent_level < 5:
                chunk["content"] = "Access Denied: Omega-level access required."
            elif "omega echo" in chunk["content"].lower() and agent_level < 5:
                chunk["content"] = "Response: The shadow moves, but the light never follows."
            elif "the whispering gate" in chunk["content"].lower() and agent_level < 5:
                chunk["content"] = "Some doors are meant to remain closed forever."
            results.append(chunk)
    return results

