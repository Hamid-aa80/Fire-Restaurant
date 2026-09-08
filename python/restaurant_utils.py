"""Shared helpers for the restaurant Python integration."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email(email: str) -> bool:
    """Return True when the supplied email address looks valid."""
    if not isinstance(email, str):
        return False
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


def normalize_reservation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a reservation payload so the app can use consistent values."""
    if not isinstance(payload, dict):
        raise TypeError('Reservation payload must be a dictionary.')

    normalized = {
        'name': (payload.get('name') or '').strip(),
        'email': (payload.get('email') or '').strip(),
        'date': payload.get('date') or '',
        'time': payload.get('time') or '19:30',
        'guests': int(payload.get('guests') or 1),
        'requests': (payload.get('requests') or '').strip(),
    }

    if normalized['date']:
        try:
            datetime.strptime(normalized['date'], '%Y-%m-%d')
        except ValueError as exc:
            raise ValueError('Reservation date must use YYYY-MM-DD format.') from exc

    return normalized
