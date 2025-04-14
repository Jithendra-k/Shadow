import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag_searcher import search_rag

query = "How do I activate protocol zeta?"
results = search_rag(query)

print("🔎 Top Results:")
for r in results:
    print(f"📄 {r['source']} | {r['id']}")
    print(r['content'])
    print("------")
