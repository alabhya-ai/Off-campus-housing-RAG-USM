"""Embed chunks with bge-small-en-v1.5 and store/query them in ChromaDB."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
    TOP_K,
)
from ingest import Chunk, chunk_documents


@dataclass
class Retrieved:
    text: str
    source: str
    position: int
    distance: float


_model: Optional[SentenceTransformer] = None
_client = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def get_client():
    global _client
    if _client is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _client = chromadb.PersistentClient(
            path=str(CHROMA_DIR),
            settings=Settings(anonymized_telemetry=False),
        )
    return _client


def _embed(texts: list[str]) -> list[list[float]]:
    model = get_model()
    embs = model.encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )
    return embs.tolist()


def embed_and_store(rebuild: bool = True) -> int:
    """Load + chunk + embed every doc into Chroma. Returns chunk count."""
    client = get_client()
    if rebuild:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    chunks: list[Chunk] = chunk_documents()
    if not chunks:
        raise RuntimeError(
            "No chunks produced — did you run `python scrape.py` first?"
        )

    batch = 64
    for i in range(0, len(chunks), batch):
        block = chunks[i : i + batch]
        collection.add(
            ids=[c.chunk_id for c in block],
            documents=[c.text for c in block],
            embeddings=_embed([c.text for c in block]),
            metadatas=[
                {"source": c.source, "position": c.position} for c in block
            ],
        )
    return len(chunks)


def retrieve(query: str, k: int = TOP_K) -> list[Retrieved]:
    """Top-k semantic search. Smaller distance = closer match."""
    client = get_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    q_emb = _embed([query])
    res = collection.query(
        query_embeddings=q_emb,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    docs = res.get("documents", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    dists = res.get("distances", [[]])[0]
    out = []
    for text, meta, dist in zip(docs, metas, dists):
        out.append(
            Retrieved(
                text=text,
                source=meta.get("source", "?"),
                position=int(meta.get("position", -1)),
                distance=float(dist),
            )
        )
    return out


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Build the vector store, or query it.")
    parser.add_argument("--build", action="store_true", help="rebuild the index")
    parser.add_argument("--query", type=str, help="query the index")
    parser.add_argument("--k", type=int, default=TOP_K)
    args = parser.parse_args()

    if args.build:
        n = embed_and_store(rebuild=True)
        print(f"Indexed {n} chunks into ChromaDB at {CHROMA_DIR}.")

    if args.query:
        results = retrieve(args.query, k=args.k)
        print(f'\nQuery: "{args.query}"')
        for i, r in enumerate(results, 1):
            print(f"\n[{i}] source={r.source}  pos={r.position}  distance={r.distance:.4f}")
            print(r.text[:400] + ("…" if len(r.text) > 400 else ""))


if __name__ == "__main__":
    main()
