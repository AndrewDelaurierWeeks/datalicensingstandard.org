#!/usr/bin/env python3
"""Validate a TDLS-AI Vendor Declaration against its schema (JSON Schema 2020-12), or convert an outside record.

Install: pip install jsonschema rfc3339-validator
Usage:   python3 validate.py tdls-ai-vendor-declaration.schema.json declaration.json
         python3 validate.py convert record.json
Exit 0 when valid; 1 with every error listed when not; 2 when the validator cannot
run. The validator refuses to run without the date and date-time format checks, or
with a library whose date check accepts a date that is not written YYYY-MM-DD.

convert reads a record in the form of OASIS Data Provenance Metadata Version 1.0
(Committee Specification Draft 01) and prints a partial declaration. It moves text
only: it prints each field it carried, writes the Use elements consent and copyright
into rights_basis.basis_detail, and leaves the rest, among them the Use element
classification and the Provenance element sub-provenance, for the vendor. A
converted declaration is incomplete and unsigned. It meets no tier until a named person
at the vendor completes and signs it. Exit 0 when a partial declaration was printed.
MIT License.
"""
import json, sys

def cannot_run(message):
    print(message, file=sys.stderr)
    sys.exit(2)

def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        cannot_run(f"cannot read {path}: {e.strerror}")
    except ValueError as e:
        cannot_run(f"cannot read {path} as JSON: {e}")

def first_text(value):
    """The first plain string inside an OASIS value (a string, a list, or an object with a description)."""
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, list):
        for item in value:
            found = first_text(item)
            if found:
                return found
    if isinstance(value, dict):
        for key in ("legal-name", "name", "long-description", "content", "value", "code"):
            found = first_text(value.get(key))
            if found:
                return found
    return None

def all_text(value):
    out = []
    for item in (value if isinstance(value, list) else [value]):
        found = first_text(item)
        if found and found not in out:
            out.append(found)
    return out

def from_oasis(path):
    rec = load(path)
    if not isinstance(rec, dict) or not isinstance(rec.get("source"), dict):
        cannot_run(f"{path} is not a Data Provenance Metadata record: no \"source\" object")
    src, prov, use = rec["source"], rec.get("provenance") or {}, rec.get("use") or {}
    comp, notes = {}, []
    def put(target, key, value, origin, cls):
        if value:
            target[key] = value
            notes.append(f"{origin} -> components[].{key if target is comp else 'rights_basis.' + key} ({cls})")
    ident = src.get("id")
    put(comp, "component_id", first_text((ident or {}).get("uuids") if isinstance(ident, dict) else ident) or first_text(src.get("name") or src.get("title")), "source.id", "carried")
    about = src.get("about") if "about" in src else src.get("description")
    put(comp, "description", first_text(src.get("name") or src.get("title")) if not about else first_text(about), "source.description", "carried")
    put(comp, "source", "; ".join(all_text(prov.get("source")) + all_text(src.get("issuer"))), "provenance.source, source.issuer", "stricter")
    put(comp, "collection_method", "; ".join(all_text(prov.get("generation-method"))), "provenance.generation-method", "carried")
    put(comp, "custodians", all_text(prov.get("origin")), "provenance.origin", "stricter")
    rights = {}
    put(rights, "terms_traveling", "; ".join(all_text(use.get("license"))), "use.license", "carried")
    consent = all_text(use.get("consents") if "consents" in use else use.get("consent"))
    put(rights, "basis_detail", "; ".join(consent + all_text(use.get("copyright"))), "use.consent, use.copyright", "stricter")
    if rights:
        comp["rights_basis"] = rights
    partial = {"schema_version": "0.3.0", "components": [comp]}
    risk = all_text([t.get("tool-used") if isinstance(t, dict) else t for t in (use.get("data-risk-reducing") or [])])
    if risk:
        partial["de_identification"] = {"method": "; ".join(risk)}
        notes.append("use.data-risk-reducing -> de_identification.method (stricter)")
    print(json.dumps(partial, indent=2, ensure_ascii=False))
    for note in notes:
        print("converted: " + note, file=sys.stderr)
    print("partial and unsigned: this meets no tier until a named person at the vendor completes and signs it", file=sys.stderr)
    return 0

def main(schema_path, doc_path):
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from jsonschema.exceptions import SchemaError
        import rfc3339_validator  # noqa: F401  (enables the date-time format check)
    except ImportError:
        cannot_run("install the validator and its format checks: pip install jsonschema rfc3339-validator")
    schema = load(schema_path)
    doc = load(doc_path)
    if not isinstance(schema, dict) or "$id" not in schema:
        cannot_run(f"{schema_path} is not a schema with an $id; the schema is the first argument")
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as e:
        cannot_run(f"{schema_path} is not a valid schema: {e.message}")
    checker = FormatChecker()
    strict = ({"date", "date-time"} <= set(checker.checkers)
              and checker.conforms("2000-01-01", "date") and checker.conforms("2000-01-01T00:00:00Z", "date-time")
              and not checker.conforms("20000101", "date") and not checker.conforms("yesterday", "date-time"))
    if not strict:
        cannot_run("format checks unavailable or lenient: pip install --upgrade jsonschema rfc3339-validator")
    v = Draft202012Validator(schema, format_checker=checker)
    errors = sorted(v.iter_errors(doc), key=lambda e: list(e.path))
    if not errors:
        print(f"valid: {doc_path} conforms to {schema.get('title')} ({schema.get('$id')})")
        return 0
    for e in errors:
        where = "/".join(str(p) for p in e.path) or "(root)"
        print(f"invalid at {where}: {e.message}")
    return 1

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "convert":
        sys.exit(from_oasis(sys.argv[2]))
    if len(sys.argv) != 3:
        cannot_run(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
