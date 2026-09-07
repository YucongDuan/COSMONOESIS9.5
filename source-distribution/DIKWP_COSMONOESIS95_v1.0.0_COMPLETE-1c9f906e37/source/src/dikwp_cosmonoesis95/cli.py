from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
from typing import Any

from .claim_audit import audit_claims, split_claims
from .compiler import compile_system
from .consciousness import assess_candidate
from .contact import evaluate_observation
from .mappings import civilization_profiles, tradition_profiles, universal_centroid
from .normalization import compare_concepts, normalize_concept
from .registries import load_registry, validate_registries
from .utils import load_json, read_json_records, save_json
from .verify import verify_output_dir


def _json_print(obj: Any, *, stream=None) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2), file=stream or sys.stdout)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="cosmonoesis95", description="DIKWP-normalized universal consciousness, religion/civilization mapping and reality-contact system")
    sub = p.add_subparsers(dest="command", required=True)

    compile_p = sub.add_parser("compile", help="Compile the complete system bundle and dashboard")
    compile_p.add_argument("--out", default="outputs/cosmonoesis_demo")
    compile_p.add_argument("--claims")
    compile_p.add_argument("--candidates")
    compile_p.add_argument("--observation")

    demo_p = sub.add_parser("demo", help="Compile bundled demonstration data")
    demo_p.add_argument("--out", default="outputs/cosmonoesis_demo")

    norm_p = sub.add_parser("normalize", help="Normalize a concept into DIKWP space")
    norm_p.add_argument("term")
    norm_p.add_argument("--context", default="")
    norm_p.add_argument("--tradition")

    cmp_p = sub.add_parser("compare", help="Compare two concepts in the unified DIKWP space")
    cmp_p.add_argument("term_a")
    cmp_p.add_argument("term_b")
    cmp_p.add_argument("--context-a", default="")
    cmp_p.add_argument("--context-b", default="")
    cmp_p.add_argument("--tradition-a")
    cmp_p.add_argument("--tradition-b")

    audit_p = sub.add_parser("audit", help="Audit claims from text or JSON")
    group = audit_p.add_mutually_exclusive_group(required=True)
    group.add_argument("--text")
    group.add_argument("--file")
    audit_p.add_argument("--out")

    assess_p = sub.add_parser("assess", help="Assess a consciousness candidate JSON")
    assess_p.add_argument("input")
    assess_p.add_argument("--out")

    contact_p = sub.add_parser("contact", help="Evaluate an anomalous-signal observation JSON")
    contact_p.add_argument("input")
    contact_p.add_argument("--out")

    map_p = sub.add_parser("map", help="Print normalized traditions or civilizations")
    map_p.add_argument("kind", choices=["traditions", "civilizations", "centroid"])
    map_p.add_argument("--out")

    verify_p = sub.add_parser("verify", help="Verify a compiled output directory")
    verify_p.add_argument("output_dir")

    serve_p = sub.add_parser("serve", help="Serve a compiled dashboard on loopback only")
    serve_p.add_argument("directory")
    serve_p.add_argument("--host", choices=["127.0.0.1", "localhost", "::1"], default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8765)

    sub.add_parser("doctor", help="Validate runtime and bundled registries")
    sub.add_parser("principles", help="Print the 20 open-ultimate working principles")
    sub.add_parser("summary", help="Print system architecture summary")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command in {"compile", "demo"}:
            bundle = compile_system(args.out, claims_path=getattr(args, "claims", None), candidates_path=getattr(args, "candidates", None), observation_path=getattr(args, "observation", None))
            _json_print({
                "status": "ok", "compilation_id": bundle["compilation_id"], "bundle_digest": bundle["bundle_digest"],
                "dashboard": str((Path(args.out) / "dashboard.html").resolve()),
                "report": str((Path(args.out) / "FULL_SYSTEM_REPORT_CN.md").resolve()),
                "traditions": len(bundle["tradition_mappings"]), "civilizations": len(bundle["civilization_mappings"]),
                "automatic_external_action_authority": 0,
            })
            return 0
        if args.command == "normalize":
            _json_print(normalize_concept(args.term, context=args.context, tradition_id=args.tradition))
            return 0
        if args.command == "compare":
            _json_print(compare_concepts(args.term_a, args.term_b, context_a=args.context_a, context_b=args.context_b, tradition_a=args.tradition_a, tradition_b=args.tradition_b))
            return 0
        if args.command == "audit":
            if args.text is not None:
                claims = split_claims(args.text)
            else:
                path = Path(args.file)
                if path.suffix.lower() == ".json":
                    claims = read_json_records(path)
                else:
                    claims = split_claims(path.read_text(encoding="utf-8"))
            result = audit_claims(claims)
            if args.out:
                save_json(args.out, result)
            _json_print(result)
            return 0
        if args.command == "assess":
            result = assess_candidate(load_json(args.input))
            if args.out:
                save_json(args.out, result)
            _json_print(result)
            return 0
        if args.command == "contact":
            result = evaluate_observation(load_json(args.input))
            if args.out:
                save_json(args.out, result)
            _json_print(result)
            return 0
        if args.command == "map":
            if args.kind == "traditions": result = {"traditions": tradition_profiles()}
            elif args.kind == "civilizations": result = {"civilizations": civilization_profiles()}
            else: result = universal_centroid()
            if args.out:
                save_json(args.out, result)
            _json_print(result)
            return 0
        if args.command == "verify":
            result = verify_output_dir(args.output_dir)
            _json_print(result)
            return 0 if result["valid"] else 2
        if args.command == "doctor":
            result = validate_registries()
            result.update({"python": sys.version.split()[0], "status": "ok", "automatic_external_action_authority": 0})
            _json_print(result)
            return 0
        if args.command == "principles":
            _json_print(load_registry("principles"))
            return 0
        if args.command == "summary":
            _json_print({
                "system": "DIKWP-COSMONOESIS 9.5",
                "loop": "D→I→K→W→P→action/practice→reality return→calibration→revision/retirement",
                "normalization": "all religious, civilizational, scientific and philosophical concepts are placed inside one DIKWP coordinate space",
                "permanent_outside_untranslatable_residual": False,
                "consciousness_policy": "multi-model evidence compatibility; no binary certificate",
                "external_action_authority": 0,
            })
            return 0
        if args.command == "serve":
            directory = Path(args.directory).resolve()
            if not directory.is_dir():
                raise FileNotFoundError(directory)
            handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
            server = ThreadingHTTPServer((args.host, args.port), handler)
            print(f"Serving {directory} at http://{args.host}:{args.port}/dashboard.html", file=sys.stderr)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                pass
            finally:
                server.server_close()
            return 0
        raise RuntimeError("Unhandled command")
    except Exception as exc:
        _json_print({"status": "error", "error": str(exc), "automatic_external_action_authority": 0}, stream=sys.stderr)
        return 2
