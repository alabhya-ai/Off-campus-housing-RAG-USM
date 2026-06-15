"""Gradio UI for the USM Off-Campus Housing RAG."""
from __future__ import annotations

import gradio as gr

from config import TOP_K
from generator import generate_response


def handle_query(question: str, k: int):
    question = (question or "").strip()
    if not question:
        return "Please enter a question.", ""

    ans = generate_response(question, k=int(k))
    sources_md = "\n".join(f"- **{s}**" for s in ans.sources) or "_(no sources retrieved)_"
    retrieved_md_parts = []
    for i, r in enumerate(ans.retrieved, 1):
        snippet = r.text[:500] + ("…" if len(r.text) > 500 else "")
        retrieved_md_parts.append(
            f"**[{i}] {r.source}**  _(distance {r.distance:.3f})_\n\n{snippet}"
        )
    retrieved_md = "\n\n---\n\n".join(retrieved_md_parts) or "_(none)_"
    return ans.answer, f"### Sources\n{sources_md}\n\n### Retrieved chunks\n{retrieved_md}"


def build_demo() -> gr.Blocks:
    with gr.Blocks(title="USM Off-Campus Housing — Unofficial Guide") as demo:
        gr.Markdown(
            "# USM Off-Campus Housing — Unofficial Guide\n"
            "Ask plain-language questions about off-campus apartments near the "
            "University of Southern Mississippi. Answers are grounded only in "
            "the scraped documents."
        )
        with gr.Row():
            question = gr.Textbox(
                label="Your question",
                placeholder="e.g. Which apartments are within a 25 minute walk to campus?",
                lines=2,
                scale=4,
            )
            k = gr.Slider(
                minimum=1, maximum=10, value=TOP_K, step=1,
                label="Top-k chunks", scale=1,
            )
        ask = gr.Button("Ask", variant="primary")
        answer = gr.Textbox(label="Answer", lines=10)
        sources = gr.Markdown(label="Sources + retrieved chunks")

        ask.click(handle_query, inputs=[question, k], outputs=[answer, sources])
        question.submit(handle_query, inputs=[question, k], outputs=[answer, sources])
    return demo


if __name__ == "__main__":
    build_demo().launch()
