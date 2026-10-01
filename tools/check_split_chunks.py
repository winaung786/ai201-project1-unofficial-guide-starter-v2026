#!/usr/bin/env python3
"""Record three new inspections of the six chunks named in criterion 4.

No embedding/model calls. Structural checks accompany the exact source and
chunk text; human review is still needed for sentence meaning and boundaries.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config
from chunker import split_documents
from ingest import load_documents

SOURCES = ("housing_innisfree_hall.txt", "housing_morrow_house.txt", "housing_old_brewhouse.txt")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    records = {
        "when_utc": now.isoformat(), "label": args.label, "corpus": config.CORPUS,
        "runs": 3, "model_calls": 0, "embedding_calls": 0,
        "produced_by": "tools/check_split_chunks.py::main via chunker.py::split_documents",
        "method": "Three fresh structural inspections; review source/chunk text manually for criterion 4",
        "rows": [],
    }
    for run in range(1, 4):
        documents = {document.source: document for document in load_documents(config.CORPUS)}
        for source in SOURCES:
            document = documents[source]
            title, _, body = document.text.partition("\n\n")
            original = " ".join(body.split())
            chunks = split_documents([document])
            rows = []
            for chunk in chunks:
                part = " ".join(chunk.text.partition("\n\n")[2].split())
                segments = re.split(r'(?<=[.!?])\s+(?=[A-Z“"\'])', part)
                rows.append({
                    "label": chunk.label, "source": chunk.source, "text": chunk.text,
                    "produced_by": chunk.produced_by,
                    "checks": {
                        "source_matches": chunk.source == source,
                        "title_matches": chunk.text.startswith(title + "\n\n"),
                        "ends_sentence": part.endswith((".", "!", "?")),
                        "all_segments_in_original": all(segment.strip() in original for segment in segments),
                    },
                })
            passed = len(rows) == 2 and all(all(row["checks"].values()) for row in rows)
            records["rows"].append({
                "run": run, "source": source, "original_text": document.text,
                "original_sha256": hashlib.sha256((config.corpus_path() / source).read_bytes()).hexdigest(),
                "chunks": rows, "structural_checks_passed": passed,
            })
        print(f"run {run}: {sum(row['structural_checks_passed'] for row in records['rows'] if row['run'] == run)}/3 posts passed structural checks")
    label = re.sub(r"[^A-Za-z0-9_-]", "-", args.label)
    path = config.RESULTS_DIR / f"chunks_{now.strftime('%Y%m%dT%H%M%S%fZ')}_{label}.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        json.dump(records, stream, indent=2, ensure_ascii=False)
        stream.write("\n")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
