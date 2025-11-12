"""
Minimal compatibility module providing the subset of ``cgi`` that modern
third-party libraries (such as ``httpx``) still import.  Python 3.13 removed
the stdlib ``cgi`` module, so we provide a lightweight replacement that
implements ``parse_header`` which is the only helper required by those
dependencies.
"""

from __future__ import annotations

from typing import Dict, Tuple


def parse_header(line: str) -> Tuple[str, Dict[str, str]]:
    """
    Parse a Content-Type like header.

    Replicates the behaviour provided by ``cgi.parse_header`` in previous
    Python versions.

    Args:
        line: Header value to parse, e.g. ``'text/html; charset=utf-8'``.

    Returns:
        Tuple of (primary value, parameter dictionary).
    """
    if not line:
        return "", {}

    parts = [part.strip() for part in line.split(";")]
    value = parts[0]
    params: Dict[str, str] = {}

    for param in parts[1:]:
        if not param or "=" not in param:
            continue
        key, val = param.split("=", 1)
        key = key.strip().lower()
        val = val.strip().strip('"').strip("'")
        params[key] = val

    return value, params


__all__ = ["parse_header"]

