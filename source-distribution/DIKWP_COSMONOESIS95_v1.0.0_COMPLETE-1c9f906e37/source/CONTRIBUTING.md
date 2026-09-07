# Contributing

Contributions are welcome for:

- branch-specific religious and philosophical mappings;
- improved primary-source provenance;
- additional consciousness theories and discriminating tests;
- stronger claim-audit rules;
- localization and accessibility;
- deterministic tests and security hardening.

Every mapping contribution must remain inside DIKWP and must not infer doctrinal identity from vector similarity. Include context, source, confidence and the consequences of changing the vector.

Run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
python run.py demo --out outputs/cosmonoesis_demo
python run.py verify outputs/cosmonoesis_demo
```
