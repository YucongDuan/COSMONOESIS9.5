from __future__ import annotations

from datetime import datetime, timezone
from html import escape as html_escape
from importlib.resources import files
import hashlib
import json
import math
import re
import unicodedata
from pathlib import Path
from typing import Any, Iterable, Iterator


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def sha256_obj(obj: Any) -> str:
    return sha256_text(canonical_json(obj))


def stable_id(prefix: str, obj: Any, length: int = 20) -> str:
    return f"{prefix}-{sha256_obj(obj)[:length]}"


def normalize_text(text: Any) -> str:
    value = unicodedata.normalize("NFKC", str(text or ""))
    value = value.replace("\u00a0", " ")
    value = re.sub(r"[\t\r ]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str | Path, obj: Any) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def save_text(path: str | Path, text: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return str(p)


def load_bundled_json(name: str) -> Any:
    resource = files("dikwp_cosmonoesis95.data").joinpath(name)
    return json.loads(resource.read_text(encoding="utf-8"))


def clamp(value: Any, low: float = 0.0, high: float = 1.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return low
    return max(low, min(high, number))


def normalize_weights(weights: dict[str, Any], allowed: set[str] | None = None) -> dict[str, float]:
    cleaned: dict[str, float] = {}
    for key, raw in weights.items():
        if allowed is not None and key not in allowed:
            raise ValueError(f"Coordinate outside DIKWP ontology: {key}")
        value = max(0.0, float(raw))
        if value:
            cleaned[str(key)] = value
    total = sum(cleaned.values())
    if total <= 0:
        raise ValueError("A semantic vector must contain at least one positive coordinate")
    return {k: round(v / total, 12) for k, v in sorted(cleaned.items())}


def dot(a: dict[str, float], b: dict[str, float]) -> float:
    return sum(a.get(k, 0.0) * b.get(k, 0.0) for k in set(a) | set(b))


def norm(a: dict[str, float]) -> float:
    return math.sqrt(sum(v * v for v in a.values()))


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    denominator = norm(a) * norm(b)
    return dot(a, b) / denominator if denominator else 0.0


def l1_distance(a: dict[str, float], b: dict[str, float]) -> float:
    return sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in set(a) | set(b))


def top_items(weights: dict[str, float], limit: int = 8) -> list[tuple[str, float]]:
    return sorted(weights.items(), key=lambda item: (-item[1], item[0]))[:limit]


def html(value: Any) -> str:
    return html_escape(str(value if value is not None else ""), quote=True)


def iter_files(root: str | Path, *, exclude_names: set[str] | None = None) -> Iterator[Path]:
    base = Path(root)
    excluded = exclude_names or set()
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.name not in excluded:
            yield path


def manifest_for(root: str | Path, *, exclude_names: set[str] | None = None) -> dict[str, Any]:
    base = Path(root)
    excluded = (exclude_names or set()) | {"MANIFEST.json", "VERIFY.txt"}
    records = []
    for path in iter_files(base, exclude_names=excluded):
        records.append({
            "path": path.relative_to(base).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256_bytes(path.read_bytes()),
        })
    result = {"algorithm": "sha256", "file_count": len(records), "files": records}
    result["manifest_digest"] = sha256_obj(result)
    return result


def read_json_records(path: str | Path) -> list[dict[str, Any]]:
    obj = load_json(path)
    if isinstance(obj, list):
        return [dict(item) for item in obj]
    if isinstance(obj, dict):
        for key in ("claims", "records", "systems", "concepts", "observations"):
            value = obj.get(key)
            if isinstance(value, list):
                return [dict(item) for item in value]
    raise ValueError(f"Expected a JSON array or recognized record container in {path}")
