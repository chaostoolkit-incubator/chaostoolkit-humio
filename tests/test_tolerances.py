from chaoshumio.tolerances import (
    field_value_above,
    field_value_between,
    field_value_under,
)


def test_field_value_under_ok() -> None:
    value = [{"_count": 5}]
    assert field_value_under(value, "_count", 6) is True


def test_field_value_under_ko() -> None:
    value = [{"_count": 8}]
    assert field_value_under(value, "_count", 6) is False


def test_field_value_above_ok() -> None:
    value = [{"_count": 5}]
    assert field_value_above(value, "_count", 4) is True


def test_field_value_above_ko() -> None:
    value = [{"_count": 3}]
    assert field_value_above(value, "_count", 4) is False


def test_field_value_between_ok() -> None:
    value = [{"_count": 5}]
    assert field_value_between(value, "_count", 4, 6) is True


def test_field_value_between_ko() -> None:
    value = [{"_count": 3}]
    assert field_value_between(value, "_count", 4, 6) is False
