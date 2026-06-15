"""Central configuration for the Off-Campus Housing RAG system."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

DOCUMENTS_DIR = ROOT / "documents"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "usm_offcampus_housing"

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

CHUNK_SIZE_TOKENS = 300
CHUNK_OVERLAP_TOKENS = 30

TOP_K = 10

GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_TEMPERATURE = 0.2
GROQ_MAX_TOKENS = 800
