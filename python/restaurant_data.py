"""Sample restaurant data used by the Python and Django integration."""

from __future__ import annotations

from typing import Any


def sample_menu() -> list[dict[str, Any]]:
    return [
        {
            'name': 'Smoked Ribeye',
            'category': 'Mains',
            'description': 'Fire-kissed ribeye served with pepper butter.',
            'price': 29.95,
            'is_chefs_pick': True,
        },
        {
            'name': 'Citrus Salmon',
            'category': 'Mains',
            'description': 'Charred salmon with fennel and herb glaze.',
            'price': 24.50,
            'is_chefs_pick': False,
        },
        {
            'name': 'Smoked Brûlée',
            'category': 'Desserts',
            'description': 'A creamy torch-finished dessert with caramel notes.',
            'price': 9.75,
            'is_chefs_pick': True,
        },
    ]


def sample_reservations() -> list[dict[str, Any]]:
    return [
        {
            'name': 'Alicia Reed',
            'email': 'alicia@example.com',
            'date': '2026-09-12',
            'time': '19:30',
            'guests': 2,
            'requests': 'Window table if possible',
        },
        {
            'name': 'Noah Stone',
            'email': 'noah@example.com',
            'date': '2026-09-13',
            'time': '20:00',
            'guests': 4,
            'requests': 'Birthday setup',
        },
    ]


if __name__ == '__main__':
    print({'menu': sample_menu(), 'reservations': sample_reservations()})
