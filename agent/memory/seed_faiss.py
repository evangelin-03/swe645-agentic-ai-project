from agent.memory.faiss_store import FaissMemory
m = FaissMemory()
m.store_document("doc1", "Project X summary: This project builds an agent to summarize docs.", {"title":"proj-x"})
m.store_document("doc2", "Notes: Add tests and demo video. Remember to commit to GitHub.", {"title":"notes"})
print("Seeded FAISS with 2 documents.")
