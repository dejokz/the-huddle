"""
Pre-computed Embeddings Loader
Loads embeddings from JSON files (no PyTorch/API needed)
"""

import json
import hashlib
import struct
import numpy as np
from typing import List, Union
from pathlib import Path

def deterministic_embedding(text: str, dim: int = 384) -> list:
    """Generate deterministic pseudo-embeddings using SHA-256 hash (process-stable)"""
    h = hashlib.sha256(text.encode("utf-8")).digest()
    seed = struct.unpack("<I", h[:4])[0]
    rng = np.random.RandomState(seed)
    vec = rng.randn(dim)
    vec = vec / np.linalg.norm(vec)
    return vec.tolist()

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))

class LocalEmbedding:
    """
    Pre-computed embeddings loader
    Uses deterministic embeddings for queries, matches against pre-computed data
    """
    
    _instance = None
    _data = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LocalEmbedding, cls).__new__(cls)
            cls._instance._load_data()
        return cls._instance
    
    def _load_data(self):
        """Load pre-computed embeddings from JSON, auto-detecting sport prefixes."""
        data_dir = Path(__file__).parent.parent / "data"
        
        for file_path in data_dir.glob("*_embeddings.json"):
            # Filename pattern: {sport}_{collection}_embeddings.json
            # e.g., cricket_match_moments_embeddings.json
            stem = file_path.stem  # removes .json
            collection = stem.replace("_embeddings", "")
            try:
                with open(file_path, encoding="utf-8") as f:
                    self._data[collection] = json.load(f)
                print(f"[LocalEmbedding] Loaded {collection}: {len(self._data[collection])} items")
            except Exception as e:
                print(f"[LocalEmbedding] Warning: failed to load {file_path}: {e}")
                self._data[collection] = []
    
    def encode(self, text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embedding for query text
        Uses deterministic hash-based embeddings
        """
        if isinstance(text, str):
            return deterministic_embedding(text)
        else:
            return [deterministic_embedding(t) for t in text]
    
    def get_collection_data(self, collection_name: str) -> list:
        """Get pre-computed data for a collection"""
        return self._data.get(collection_name, [])
    
    @property
    def dimension(self) -> int:
        return 384


# Convenience functions
def get_embedding(text: str) -> List[float]:
    """Quick function to get embedding for a single text"""
    return deterministic_embedding(text)
