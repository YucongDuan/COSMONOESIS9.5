"""DIKWP-COSMONOESIS 9.5 public API."""

from .compiler import compile_system
from .normalization import normalize_concept, compare_concepts
from .claim_audit import audit_claims
from .consciousness import assess_candidate

__all__ = [
    "compile_system",
    "normalize_concept",
    "compare_concepts",
    "audit_claims",
    "assess_candidate",
]

__version__ = "1.0.0"
SYSTEM_NAME = "DIKWP-COSMONOESIS 9.5"
MESH_MODE = "MESH95_ASYMMETRY_PROTECTIVE_AGENCY_NONPSEUDONEUTRAL_RESPONSIBILITY_CLOSURE"
AUTOMATIC_EXTERNAL_ACTION_AUTHORITY = 0
