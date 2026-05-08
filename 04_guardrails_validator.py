"""Step 4 - Custom Guardrails validators for PII and JSON repair."""

from __future__ import annotations

import json
import re

try:
    from guardrails import Guard, OnFailAction, Validator, register_validator
except Exception:  # pragma: no cover - compatibility fallback
    from guardrails import Guard, Validator, register_validator
    from guardrails.validator_base import OnFailAction

try:
    from guardrails.validators import FailResult, PassResult
except Exception:  # pragma: no cover - compatibility fallback
    from guardrails.validator_base import FailResult, PassResult


@register_validator(name="pii-detector", data_type="string")
class PIIDetector(Validator):
    """Detect and redact common PII patterns using regex."""

    PII_PATTERNS = {
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "PHONE": r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]\d{4}\b",
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "CREDIT_CARD": r"\b(?:\d[ -]*?){13,19}\b",
    }

    def validate(self, value: str, metadata: dict | None = None):
        redacted_text = value
        found_types = []

        for pii_type, pattern in self.PII_PATTERNS.items():
            matches = re.findall(pattern, redacted_text)
            if not matches:
                continue
            found_types.append(pii_type)
            redacted_text = re.sub(pattern, "[REDACTED]", redacted_text)

        if found_types:
            print(f"  ⚠️  Redacted PII types: {', '.join(found_types)}")
            return FailResult(error_message="PII detected", fix_value=redacted_text)

        return PassResult(value_override=value)


@register_validator(name="json-formatter", data_type="string")
class JSONFormatter(Validator):
    """Validate JSON strings and repair common formatting issues."""

    @staticmethod
    def _repair(text: str) -> str:
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()
        text = text.replace("'", '"')
        text = re.sub(r",\s*([}\]])", r"\1", text)
        return text

    def validate(self, value: str, metadata: dict | None = None):
        try:
            parsed = json.loads(value)
            return PassResult(value_override=json.dumps(parsed, indent=2, sort_keys=True))
        except json.JSONDecodeError:
            pass

        try:
            repaired_text = self._repair(value)
            parsed = json.loads(repaired_text)
            print("  🔧 JSON repaired successfully")
            return PassResult(value_override=json.dumps(parsed, indent=2, sort_keys=True))
        except json.JSONDecodeError as exc:
            fallback = json.dumps({"error": str(exc), "raw": value}, indent=2)
            return FailResult(error_message=f"Invalid JSON after repair attempt: {exc}", fix_value=fallback)


def demo_pii_guard() -> None:
    """Run a small PII redaction demo."""

    print("\n" + "=" * 55)
    print("  PII Detection Demo")
    print("=" * 55)

    guard = Guard().use(PIIDetector(on_fail=OnFailAction.FIX))

    test_cases = [
        ("Email", "Contact John at john.doe@example.com for details."),
        ("Phone", "Call our support line at (555) 867-5309."),
        ("SSN", "Patient SSN is 123-45-6789 on file."),
        ("Credit Card", "Payment made with card 4532 1234 5678 9010."),
        ("Multi-PII", "Email: alice@example.com, Phone: 555-123-4567"),
        ("Clean", "No sensitive information in this text."),
    ]

    for label, text in test_cases:
        result = guard.validate(text)
        print(f"\n[{label}]")
        print(f"  Input:  {text}")
        print(f"  Output: {result.validated_output}")


def demo_json_guard() -> None:
    """Run a JSON repair demo."""

    print("\n" + "=" * 55)
    print("  JSON Formatting Demo")
    print("=" * 55)

    guard = Guard().use(JSONFormatter(on_fail=OnFailAction.FIX))

    test_cases = [
        ("Valid JSON", '{"name": "Alice", "age": 30}'),
        ("Markdown fences", '```json\n{"name": "Bob"}\n```'),
        ("Single quotes", "{'name': 'Charlie', 'score': 95}"),
        ("Trailing comma", '{"key": "value",}'),
        ("Truly invalid", "This is not JSON at all: ??? {]"),
    ]

    for label, text in test_cases:
        result = guard.validate(text)
        status = "✅ Pass" if result.validation_passed else "❌ Fail"
        print(f"\n[{label}] {status}")
        print(f"  Input:  {text[:60]}")
        print(f"  Output: {str(result.validated_output)[:120]}")


def main() -> None:
    print("=" * 55)
    print("  Step 4: Guardrails AI Validators")
    print("=" * 55)

    demo_pii_guard()
    demo_json_guard()

    print("\n✅ Step 4 complete!")


if __name__ == "__main__":
    main()
