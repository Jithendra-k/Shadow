import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import faiss

def build_rag_index():
    model = SentenceTransformer('all-MiniLM-L6-v2')

    manual_path = Path("app/knowledge_base/manual_text.txt")
    rules_path = Path("app/knowledge_base/classified_rules.json")

    manual_chunks = []
    if manual_path.exists():
        text = manual_path.read_text(encoding='utf-8')
        paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
        for i, p in enumerate(paragraphs):
            manual_chunks.append({
                "id": f"manual-{i}",
                "source": "manual_text",
                "content": p
            })

    rules_chunks = []
    if rules_path.exists():
        rules = json.loads(rules_path.read_text(encoding='utf-8'))
        for i, rule in enumerate(rules):
            rules_chunks.append({
                "id": f"rule-{i}",
                "source": "classified_rules",
                "content": f"Level {rule['level']} - Trigger: {rule['trigger']} → Response: {rule['response']}"
            })

    all_chunks = manual_chunks + rules_chunks
    corpus = [chunk["content"] for chunk in all_chunks]
    embeddings = model.encode(corpus, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "app/knowledge_base/rag_index.faiss")
    with open("app/knowledge_base/rag_metadata.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("✅ RAG index built successfully!")

if __name__ == "__main__":
    build_rag_index()
