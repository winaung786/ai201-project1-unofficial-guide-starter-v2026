"""Stage 2: title-preserving, sentence-aware chunks for short campus posts."""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    text: str
    source: str
    index: int
    produced_by: str

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(documents, chunk_size=None, overlap=None) -> list[Chunk]:
    """Original character-window algorithm, retained for comparison."""
    chunk_size = config.CHUNK_SIZE if chunk_size is None else chunk_size
    overlap = config.CHUNK_OVERLAP if overlap is None else overlap
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")
    chunks = []
    for doc in documents:
        index = 0
        for start in range(0, len(doc.text), chunk_size - overlap):
            piece = doc.text[start:start + chunk_size].strip()
            if piece:
                chunks.append(Chunk(piece, doc.source, index, "chunker.py::fallback_split"))
                index += 1
    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """Keep short posts intact; split long posts only between whole sentences.

    CHUNK_SIZE is a soft character limit including the title. CHUNK_OVERLAP
    is an upper bound on repeated whole sentences, not an exact slice. Titles
    are repeated separately. A single oversized sentence is never truncated.
    Sentence detection is a lightweight heuristic for the supplied prose,
    not a general-purpose linguistic tokenizer.
    """
    size, overlap = config.CHUNK_SIZE, config.CHUNK_OVERLAP
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require CHUNK_SIZE > 0 and 0 <= CHUNK_OVERLAP < CHUNK_SIZE")
    chunks = []
    for doc in documents:
        text = doc.text.strip()
        if not text:
            continue
        if len(text) <= size:
            chunks.append(Chunk(text, doc.source, 0, "chunker.py::split_documents"))
            continue

        first, separator, rest = text.partition("\n\n")
        # A one-line opening followed by a blank line is a title in this corpus.
        title = first if separator and "\n" not in first else ""
        body = rest if title else text
        prefix = f"{title}\n\n" if title else ""
        sentences = []
        for paragraph in re.split(r"\n\s*\n", body):
            paragraph = " ".join(paragraph.split())
            sentences.extend(s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z“"\'])', paragraph) if s)

        current = []
        pieces = []
        for sentence in sentences:
            if current and len(prefix + " ".join(current + [sentence])) > size:
                pieces.append(prefix + " ".join(current))
                trailing = []
                for previous in reversed(current):
                    candidate = [previous] + trailing
                    if len(" ".join(candidate)) > overlap:
                        break
                    trailing = candidate
                while trailing and len(prefix + " ".join(trailing + [sentence])) > size:
                    trailing.pop(0)
                current = trailing
            current.append(sentence)
        if current:
            pieces.append(prefix + " ".join(current))
        for index, piece in enumerate(pieces):
            chunks.append(Chunk(piece, doc.source, index, "chunker.py::split_documents"))
    return chunks


def describe(chunks: list[Chunk]) -> str:
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, {sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents
    print(describe(split_documents(load_documents())))
