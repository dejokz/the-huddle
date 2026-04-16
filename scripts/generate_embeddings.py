"""
Generate pre-computed embedding JSON files for any sport data module.
Usage:
    python scripts/generate_embeddings.py cricket
    python scripts/generate_embeddings.py football
    python scripts/generate_embeddings.py chess
"""

import sys
import json
import importlib.util
import uuid
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.embeddings import get_embedding


def to_uuid(item_id) -> str:
    """Convert any ID to a valid UUID string for Qdrant."""
    if isinstance(item_id, int):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(item_id)))
    # Deterministic UUID from string ID
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(item_id)))


def generate_collection_embeddings(items: list, id_key: str = "moment_id") -> list:
    """Generate embeddings for a list of dataclass instances or dicts."""
    results = []
    for item in items:
        if hasattr(item, "__dataclass_fields__"):
            payload = {}
            for key in item.__dataclass_fields__:
                val = getattr(item, key)
                if isinstance(val, (list, dict, str, int, float, bool)) or val is None:
                    payload[key] = val
                else:
                    payload[key] = str(val)
            # Choose embedding text based on available fields
            text_parts = []
            for key in ("description", "name", "match_name", "reasoning", "characteristics"):
                if key in payload and payload[key]:
                    text_parts.append(str(payload[key]))
            text = " ".join(text_parts) or json.dumps(payload)
            # Use a sensible id field
            item_id = payload.get(id_key, payload.get("player_id", payload.get("venue_id", payload.get("scenario_id", str(len(results))))))
        else:
            payload = dict(item)
            text_parts = []
            for key in ("description", "name", "match_name", "reasoning", "characteristics"):
                if key in payload and payload[key]:
                    text_parts.append(str(payload[key]))
            text = " ".join(text_parts) or json.dumps(payload)
            item_id = payload.get(id_key, payload.get("player_id", payload.get("venue_id", payload.get("scenario_id", str(len(results))))))

        vector = get_embedding(text)
        results.append({
            "id": to_uuid(item_id),
            "vector": vector,
            "payload": payload
        })
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_embeddings.py <sport>")
        sys.exit(1)

    sport = sys.argv[1]
    data_module_path = f"app.sports.{sport}.{sport}_data"
    data_dir = project_root / "data"

    try:
        # Load module directly from file to avoid triggering package __init__ imports
        file_path = project_root / "app" / "sports" / sport / f"{sport}_data.py"
        spec = importlib.util.spec_from_file_location(f"{sport}_data", file_path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[f"{sport}_data"] = mod
        spec.loader.exec_module(mod)
    except Exception as e:
        print(f"[ERROR] Could not load {file_path}: {e}")
        sys.exit(1)

    mappings = {
        "match_moments": ("get_all_moments", "moment_id"),
        "players": ("get_all_players", "player_id"),
        "venues": ("get_all_venues", "venue_id"),
        "strategies": ("get_all_strategies", "strategy_id"),
        "fantasy_scenarios": ("get_all_scenarios", "scenario_id"),
    }

    generated = []
    for collection_suffix, (getter_name, id_key) in mappings.items():
        if not hasattr(mod, getter_name):
            continue
        items = getattr(mod, getter_name)()
        if not items:
            continue
        collection_name = f"{sport}_{collection_suffix}"
        file_path = data_dir / f"{collection_name}_embeddings.json"
        embeddings = generate_collection_embeddings(items, id_key=id_key)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(embeddings, f, indent=2)
        print(f"[OK] Generated {collection_name}: {len(embeddings)} items -> {file_path.name}")
        generated.append(file_path.name)

    if not generated:
        print("[WARN] No collections generated. Check that your data module exports the expected getters.")
    else:
        print(f"[DONE] Generated {len(generated)} embedding files for {sport}.")


if __name__ == "__main__":
    main()
