"""
Set up Qdrant collections for all sports and load pre-computed embeddings.
Usage:
    python scripts/setup_qdrant.py
"""

import os
import sys
import json
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

QDRANT_URL = os.getenv("QDRANT_URL", "localhost:6333")
VECTOR_DIM = 384


def setup_collections():
    client = QdrantClient(QDRANT_URL)
    data_dir = project_root / "data"

    # Find all embedding files
    embedding_files = sorted(data_dir.glob("*_embeddings.json"))
    if not embedding_files:
        print("[WARN] No embedding files found in data/")
        return

    for file_path in embedding_files:
        collection_name = file_path.stem.replace("_embeddings", "")
        print(f"[SETUP] {collection_name} ...")

        # Load points
        with open(file_path, "r", encoding="utf-8") as f:
            points_data = json.load(f)

        # Create collection if not exists
        try:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE),
            )
            print(f"  [CREATE] Collection {collection_name} created")
        except Exception as e:
            if "already exists" in str(e).lower():
                print(f"  [EXISTS] Collection {collection_name} already exists")
            else:
                print(f"  [ERROR] Creating collection: {e}")
                continue

        # Upsert points
        points = [
            PointStruct(
                id=pt["id"],
                vector=pt["vector"],
                payload=pt["payload"],
            )
            for pt in points_data
        ]

        client.upsert(collection_name=collection_name, points=points)
        print(f"  [UPSERT] Loaded {len(points)} points into {collection_name}")

    print("[DONE] All collections set up.")


if __name__ == "__main__":
    setup_collections()
