"""Pure, repository-wide static lint routing.

Domain validators remain in their existing owner modules.  This package owns
only their common selection, read-only execution, and structured results.
"""

from .models import LintContext, LintResult, LintScope, LintSpec
from .registry import build_registry
from .runner import lint, lint_ticket, render_payload

__all__ = [
    "LintContext",
    "LintResult",
    "LintScope",
    "LintSpec",
    "build_registry",
    "lint",
    "lint_ticket",
    "render_payload",
]
