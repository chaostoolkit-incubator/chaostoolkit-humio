from typing import Any, Optional

__all__ = ["field_value_under", "field_value_above", "field_value_between"]


def field_value_under(
    value: Any = None,
    field: Optional[str] = None,
    upper: float = 0.0,
) -> bool:
    """
    Validate value at the given field to be under the given upper limit.
    """
    if not value:
        return False

    if not isinstance(value, list):
        value = [value]

    for v in value:
        current = v.get(field)
        if current is None:
            return False

        if float(current) > upper:
            return False

    return True


def field_value_above(
    value: Any = None,
    field: Optional[str] = None,
    lower: float = 0.0,
) -> bool:
    """
    Validate value at the given field to be above the given lower limit.
    """
    if not value:
        return False

    if not isinstance(value, list):
        value = [value]

    for v in value:
        current = v.get(field)
        if current is None:
            return False

        if float(current) < lower:
            return False

    return True


def field_value_between(
    value: Any = None,
    field: Optional[str] = None,
    lower: float = 0.0,
    upper: float = 0.0,
) -> bool:
    """
    Validate value at the given field to be between the lower/upper boundaries.
    """
    if not value:
        return False

    if not isinstance(value, list):
        value = [value]

    for v in value:
        current = v.get(field)
        if current is None:
            return False

        if (lower > float(current)) or (float(current) > upper):
            return False

    return True
