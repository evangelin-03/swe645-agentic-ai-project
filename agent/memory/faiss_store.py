# agent/memory/faiss_store.py
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

INDEX_DIR = os.path.join(os.path.dirname(__file__), "faiss_data")
INDEX_FILE = os.path.join(INDEX_DIR, "index.faiss")
META_FILE = os.path.join(INDEX_DIR, "meta.json")
EMBED_MODEL_NAME = os.getenv("SENTENCE_EMBEDDING_MODEL", "all-MiniLM-L6-v2")

class FaissMemory:
    def __init__(self, index_dir: str = INDEX_DIR, dim: int = 384):
        self.index_dir = index_dir
        os.makedirs(self.index_dir, exist_ok=True)
        self.index_path = INDEX_FILE
        self.meta_path = META_FILE
        self.dim = dim
        # load local embedding model (sentence-transformers)
        self.embedder = SentenceTransformer(EMBED_MODEL_NAME)
        self.meta = []
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                if os.path.exists(self.meta_path):
                    with open(self.meta_path, "r", encoding="utf8") as fh:
                        self.meta = json.load(fh)
                else:
                    self.meta = []
            except Exception as e:
                print("Warning: failed to load existing FAISS index:", e)
                self.index = faiss.IndexFlatL2(self.dim)
                self.meta = []
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []

    def _save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "w", encoding="utf8") as fh:
            json.dump(self.meta, fh, ensure_ascii=False, indent=2)

    def _embed(self, texts: List[str]) -> np.ndarray:
        embs = self.embedder.encode(texts, convert_to_numpy=True)
        embs = embs.astype("float32")
        if embs.ndim == 1:
            embs = np.expand_dims(embs, 0)
        if embs.shape[1] != self.dim:
            self.dim = embs.shape[1]
            print(f"Embedding dimension changed to {self.dim}; reinitializing index (previous vectors lost).")
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []
        return embs

    def store_document(self, doc_id: str, text: str, metadata: Dict = None):
        metadata = metadata or {}
        vec = self._embed([text])
        try:
            self.index.add(vec)
            self.meta.append({"id": doc_id, "text": text, "meta": metadata})
            self._save()
            return True
        except Exception as e:
            print("Error storing document to FAISS:", e)
            return False

    def search(self, query: str, top_k: int = 5):
        qvec = self._embed([query])
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(qvec, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.meta):
                continue
            item = self.meta[idx]
            results.append({
                "id": item.get("id"),
                "text": item.get("text"),
                "meta": item.get("meta"),
                "score": float(dist)
            })
        return results

    def list_documents(self):
        return self.meta.copy()
