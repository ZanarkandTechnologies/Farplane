"""Ticket validation orchestration."""

from __future__ import annotations

from pathlib import Path

from .models import PathBoundary, ValidationContext, ValidationPhase, ValidationReceipt
from .receipt import write_receipt
from .registry import CheckRegistry
from .select import relative_ticket, select_checks


def validate_ticket(
    *,
    root: Path,
    ticket: Path,
    phase: ValidationPhase,
    boundary: PathBoundary,
    registry: CheckRegistry,
    write: bool = True,
) -> ValidationReceipt:
    ticket = ticket.resolve()
    if not ticket.is_file():
        raise ValueError(f"ticket does not exist: {ticket}")
    text = ticket.read_text(encoding="utf-8")
    check_ids = select_checks(phase, boundary, text, root / "rules" / "validation.toml")
    context = ValidationContext(root=root.resolve(), ticket=ticket, phase=phase, boundary=boundary)
    receipt = ValidationReceipt(
        schema_version=1,
        ticket=relative_ticket(ticket, root),
        phase=phase,
        path_source=boundary.source,
        base=boundary.base,
        changed_paths=list(boundary.paths),
        selected_checks=check_ids,
    )
    for check_id in check_ids:
        spec = registry.resolve(check_id)
        receipt.results.append(spec.run(context, spec.mode))
    if write:
        write_receipt(receipt, ticket.parent / "artifacts" / "validation")
    return receipt
