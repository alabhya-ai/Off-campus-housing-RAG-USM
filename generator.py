"""Grounded response generation via Groq."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from groq import Groq

from config import GROQ_MAX_TOKENS, GROQ_MODEL, GROQ_TEMPERATURE, TOP_K
from retriever import Retrieved, retrieve

load_dotenv()

SYSTEM_PROMPT = (
    "You are an assistant that answers questions about off-campus housing near "
    "the University of Southern Mississippi (USM) in Hattiesburg, MS. "
    "You must answer using ONLY the information in the CONTEXT block below. "
    "Do not use outside knowledge, do not speculate, and do not invent facts "
    "(apartment names, prices, policies, amenities) that are not present in the context. "
    "If the context does not contain enough information to answer the question, "
    "reply exactly with: \"I don't have enough information on that.\" "
    "When you do answer, cite the source filenames you used inline like "
    "[source: filename.txt] next to each claim. Be concise."
)

USER_TEMPLATE = """CONTEXT:
{context}

QUESTION: {question}

Answer using only the CONTEXT above. Cite sources inline."""


@dataclass
class Answer:
    question: str
    answer: str
    sources: list[str]
    retrieved: list[Retrieved]


def _format_context(chunks: list[Retrieved]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(
            f"[{i}] source={c.source}  position={c.position}  distance={c.distance:.3f}\n"
            f"{c.text}"
        )
    return "\n\n---\n\n".join(parts)


_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        key = os.environ.get("GROQ_API_KEY")
        if not key:
            raise RuntimeError(
                "GROQ_API_KEY missing. Copy .env.example to .env and add your key."
            )
        _client = Groq(api_key=key)
    return _client


def generate_response(question: str, k: int = TOP_K) -> Answer:
    chunks = retrieve(question, k=k)

    if not chunks:
        return Answer(
            question=question,
            answer="I don't have enough information on that.",
            sources=[],
            retrieved=[],
        )

    context = _format_context(chunks)
    client = _get_client()
    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=GROQ_TEMPERATURE,
        max_tokens=GROQ_MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(
                context=context, question=question
            )},
        ],
    )
    raw = completion.choices[0].message.content.strip()

    seen: list[str] = []
    for c in chunks:
        if c.source not in seen:
            seen.append(c.source)

    return Answer(question=question, answer=raw, sources=seen, retrieved=chunks)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("question", nargs="+", help="ask a single question")
    parser.add_argument("--k", type=int, default=TOP_K)
    args = parser.parse_args()

    q = " ".join(args.question)
    ans = generate_response(q, k=args.k)
    print(f"\nQ: {ans.question}\n")
    print(f"A: {ans.answer}\n")
    print("Sources retrieved:")
    for s in ans.sources:
        print(f"  - {s}")


if __name__ == "__main__":
    main()
