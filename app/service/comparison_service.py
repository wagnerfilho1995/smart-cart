from decimal import Decimal, ROUND_HALF_UP

from schema.comparison_schema import ProductComparisonIN, ProductComparisonOUT, ProductItemIN
from utils.unit_normalizer import normalize_weight


def _round_currency(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _format_price(price: Decimal) -> str:
    rounded_price = _round_currency(price)
    integer_part, decimal_part = str(rounded_price).split(".")
    return f"R$ {integer_part},{decimal_part}"


def _build_best_option_message(*, name: str, brand: str | None, price: Decimal) -> str:
    brand_label = f" ({brand})" if brand else ""
    formatted_price = _format_price(price)
    return f"O produto mais vantajoso é {name}{brand_label} por {formatted_price}"


def _get_price_per_base_unit(item: ProductItemIN) -> Decimal:
    total_weight = item.quantity * item.weight
    normalized_weight, _, _ = normalize_weight(weight=total_weight, unit=item.unit)
    return _round_currency(item.price / normalized_weight)


def compare_products(payload: ProductComparisonIN) -> ProductComparisonOUT:
    best_item = payload.items[0]
    best_price_per_base_unit = _get_price_per_base_unit(best_item)

    for item in payload.items[1:]:
        price_per_base_unit = _get_price_per_base_unit(item)

        if price_per_base_unit < best_price_per_base_unit:
            best_item = item
            best_price_per_base_unit = price_per_base_unit

    return ProductComparisonOUT(
        message=_build_best_option_message(
            name=best_item.name,
            brand=best_item.brand,
            price=best_item.price,
        )
    )
