"""Load documents/*.txt and split them into token-bounded chunks.

Chunk size and overlap come from config.py (planning.md spec).
Tokenization uses the BGE embedding model's own tokenizer so token counts match
what the embedding model actually sees.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from transformers import AutoTokenizer

from config import (
    CHUNK_OVERLAP_TOKENS,
    CHUNK_SIZE_TOKENS,
    DOCUMENTS_DIR,
    EMBEDDING_MODEL,
)


@dataclass
class Chunk:
    chunk_id: str
    source: str
    position: int
    text: str


_tokenizer = None


def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        _tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
    return _tokenizer


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[tuple[str, str]]:
    """Return list of (source_filename, text) for every .txt file."""
    docs = []
    for path in sorted(documents_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        docs.append((path.name, text))
    return docs


def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE_TOKENS,
    overlap: int = CHUNK_OVERLAP_TOKENS,
) -> list[str]:
    """Token-based sliding window using the embedding model's tokenizer."""
    tok = _get_tokenizer()
    ids = tok.encode(text, add_special_tokens=False)
    if not ids:
        return []
    step = max(1, chunk_size - overlap)
    chunks = []
    for start in range(0, len(ids), step):
        window = ids[start : start + chunk_size]
        if not window:
            break
        piece = tok.decode(window, skip_special_tokens=True).strip()
        if piece:
            chunks.append(piece)
        if start + chunk_size >= len(ids):
            break
    return chunks


def chunk_documents(
    docs: Iterable[tuple[str, str]] | None = None,
) -> list[Chunk]:
    """Load all documents and split into Chunk objects with source metadata."""
    if docs is None:
        docs = load_documents()
    out: list[Chunk] = []
    for source, text in docs:
        pieces = chunk_text(text)
        for i, piece in enumerate(pieces):
            out.append(
                Chunk(
                    chunk_id=f"{source}::{i:04d}",
                    source=source,
                    position=i,
                    text=piece,
                )
            )
    return out


def main() -> None:
    chunks = chunk_documents()
    print(f"Loaded {len({c.source for c in chunks})} documents")
    print(f"Produced {len(chunks)} chunks")
    if chunks:
        print(f"Avg chunk length: {sum(len(c.text) for c in chunks) // len(chunks)} chars\n")
        print("Sample chunks:")
        for c in chunks[: min(5, len(chunks))]:
            print(f"\n--- {c.chunk_id} ---")
            print(c.text[:400])


if __name__ == "__main__":
    main()
