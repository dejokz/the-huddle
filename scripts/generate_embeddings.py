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

    service = sys.argv[1]
    data_dir = project_root / "data"

    # Try common naming patterns for the data module
    naming_candidates = [f"{service}_data.py"]
    if service == "certificates":
        naming_candidates.insert(0, "cert_data.py")
    if service == "grievances":
        naming_candidates.insert(0, "grievance_data.py")

    file_path = None
    mod = None
    for candidate in naming_candidates:
        candidate_path = project_root / "app" / "services" / service / candidate
        if candidate_path.exists():
            file_path = candidate_path
            module_name = candidate.replace(".py", "")
            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                mod = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)
                break
            except Exception as e:
                print(f"[WARN] Could not load {candidate_path}: {e}")
                continue

    if mod is None:
        print(f"[ERROR] Could not find a valid data module for service '{service}'. Tried: {naming_candidates}")
        sys.exit(1)

    # Discover available getters dynamically
    # Expected pattern: get_all_<collection>() where collection maps to cert_procedures, cert_documents, etc.
    available_getters = [name for name in dir(mod) if name.startswith("get_all_")]

    generated = []
    for getter_name in available_getters:
        items = getattr(mod, getter_name)()
        if not items:
            continue
        # collection_suffix from getter_name: get_all_procedures -> procedures
        collection_suffix = getter_name.replace("get_all_", "")
        collection_name = f"{service}_{collection_suffix}"
        file_path = data_dir / f"{collection_name}_embeddings.json"

        # Infer id_key from first item
        id_key = None
        if items:
            keys = list(items[0].keys())
            for candidate in ("step_id", "doc_id", "template_id", "office_id", "id"):
                if candidate in keys:
                    id_key = candidate
                    break
        if not id_key:
            id_key = "id"

        embeddings = generate_collection_embeddings(items, id_key=id_key)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(embeddings, f, indent=2)
        print(f"[OK] Generated {collection_name}: {len(embeddings)} items -> {file_path.name}")
        generated.append(file_path.name)

    if not generated:
        print("[WARN] No collections generated. Check that your data module exports getters like get_all_procedures, get_all_documents, etc.")
    else:
        print(f"[DONE] Generated {len(generated)} embedding files for {service}.")


if __name__ == "__main__":
    main()
