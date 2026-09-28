"""
Part 4 - Recycling Instruction Generation with RAG   [Owner: Eglen]

Retrieval: sentence-transformers (all-MiniLM-L6-v2) embeddings + FAISS index
built over policy-document chunks AND the per-category disposal instructions
from the CSV.
Generation: FLAN-T5-base conditioned on the retrieved context.

Exposes generate_instructions(category, query) -> (text, retrieved_docs),
the interface Part 5 calls. Results are modest by design (small model); the
point is that generation LEANS ON the retrieved policy text.
"""
import os, json
import joblib
from . import config as C
from . import data_prep


def _build_corpus():
    """Chunk policy docs + category disposal instructions into retrievable passages."""
    docs = []
    for p in data_prep.load_policies():
        docs.append({
            "source": p["policy_type"],
            "categories": p.get("categories_covered", []),
            "text": p["document_text"],
        })
    # add short per-category disposal tips from the CSV (dedup)
    df = data_prep.load_descriptions(split=False)
    for cat, sub in df.groupby("category"):
        tips = sorted(set(sub["disposal_instruction"].dropna()))[:5]
        if tips:
            docs.append({"source": f"{cat} disposal tips",
                         "categories": [cat],
                         "text": f"Disposal guidance for {cat}: " + " ".join(tips)})
    return docs


def build_index():
    from sentence_transformers import SentenceTransformer
    import faiss, numpy as np
    corpus = _build_corpus()
    embedder = SentenceTransformer(C.EMBED_MODEL_NAME)
    emb = embedder.encode([d["text"] for d in corpus], normalize_embeddings=True)
    index = faiss.IndexFlatIP(emb.shape[1])
    index.add(emb.astype("float32"))
    os.makedirs(C.MODELS_DIR, exist_ok=True)
    faiss.write_index(index, C.RAG_INDEX_PATH)
    joblib.dump(corpus, C.RAG_CHUNKS_PATH)
    return index, corpus


_embedder = _index = _corpus = _gen = None
def _load():
    global _embedder, _index, _corpus, _gen
    if _index is None:
        from sentence_transformers import SentenceTransformer
        from transformers import pipeline
        import faiss
        _embedder = SentenceTransformer(C.EMBED_MODEL_NAME)
        _index = faiss.read_index(C.RAG_INDEX_PATH)
        _corpus = joblib.load(C.RAG_CHUNKS_PATH)
        _gen = pipeline("text2text-generation", model=C.GEN_MODEL_NAME)


def retrieve(query, k=3, category=None):
    _load()
    q = _embedder.encode([query], normalize_embeddings=True).astype("float32")
    scores, idx = _index.search(q, k * 3)
    hits = [_corpus[i] for i in idx[0]]
    if category:  # prefer chunks that actually cover the category
        hits = sorted(hits, key=lambda d: category not in d["categories"])
    return hits[:k]


def generate_instructions(category, query=None):
    """INTEGRATION INTERFACE (Part 5). Returns (instructions_text, retrieved_docs)."""
    _load()
    query = query or f"How to recycle {category}?"
    docs = retrieve(query, k=3, category=category)
    context = "\n\n".join(f"[{d['source']}]\n{d['text']}" for d in docs)
    prompt = (
        "You are a city recycling assistant. Using ONLY the policy context below, "
        f"give clear step-by-step recycling instructions for '{category}'.\n\n"
        f"Context:\n{context}\n\nInstructions:")
    out = _gen(prompt, max_new_tokens=200, do_sample=True, temperature=0.7,
               top_p=0.9)[0]["generated_text"]
    return out, docs
