from decimal import Decimal
from enum import Enum


class MeasureCategory(str, Enum):
    WEIGHT = "weight"
    VOLUME = "volume"


WEIGHT_UNITS: dict[str, Decimal] = {
    "mg": Decimal("0.000001"),
    "g": Decimal("0.001"),
    "kg": Decimal("1"),
}

VOLUME_UNITS: dict[str, Decimal] = {
    "ml": Decimal("0.001"),
    "l": Decimal("1"),
}

BASE_UNIT_LABEL: dict[MeasureCategory, str] = {
    MeasureCategory.WEIGHT: "kg",
    MeasureCategory.VOLUME: "l",
}


def get_measure_category(unit: str) -> MeasureCategory | None:
    normalized_unit = unit.lower()
    if normalized_unit in WEIGHT_UNITS:
        return MeasureCategory.WEIGHT
    if normalized_unit in VOLUME_UNITS:
        return MeasureCategory.VOLUME
    return None


def normalize_weight(*, weight: Decimal, unit: str) -> tuple[Decimal, MeasureCategory, str]:
    normalized_unit = unit.lower()
    category = get_measure_category(normalized_unit)
    if category is None:
        raise ValueError(f"Unidade de medida não suportada: {unit}")

    conversion_factor = (
        WEIGHT_UNITS[normalized_unit]
        if category == MeasureCategory.WEIGHT
        else VOLUME_UNITS[normalized_unit]
    )
    normalized_weight = weight * conversion_factor
    base_unit = BASE_UNIT_LABEL[category]
    return normalized_weight, category, base_unit
