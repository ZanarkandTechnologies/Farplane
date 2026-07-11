"""Shared phase-aware validation kernel."""

from .models import CheckResult, PathBoundary, ValidationContext, ValidationReceipt
from .run import validate_ticket

__all__ = [
    "CheckResult",
    "PathBoundary",
    "ValidationContext",
    "ValidationReceipt",
    "validate_ticket",
]
