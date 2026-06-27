import sys
from decimal import Decimal

import pytest

sys.path.append("../../app/")

from schema.comparison_schema import ProductComparisonIN, ProductItemIN
from service.comparison_service import compare_products


def test_compare_milk_powder_itambe_is_better():
    payload = ProductComparisonIN(
        items=[
            ProductItemIN(
                name="Leite em pó",
                brand="itambe",
                price=Decimal("14.00"),
                weight=Decimal("300"),
                unit="g",
            ),
            ProductItemIN(
                name="Leite em pó",
                brand="piracanjuba",
                price=Decimal("12.00"),
                weight=Decimal("200"),
                unit="g",
            ),
        ]
    )

    result = compare_products(payload)

    assert result.message == "O produto mais vantajoso é Leite em pó (itambe) por R$ 14,00"


def test_compare_readme_example_product_b_is_better():
    payload = ProductComparisonIN(
        items=[
            ProductItemIN(
                name="Produto A",
                price=Decimal("13.00"),
                weight=Decimal("300"),
                unit="g",
            ),
            ProductItemIN(
                name="Produto B",
                price=Decimal("14.90"),
                weight=Decimal("400"),
                unit="g",
            ),
        ]
    )

    result = compare_products(payload)

    assert result.message == "O produto mais vantajoso é Produto B por R$ 14,90"


def test_compare_volume_units():
    payload = ProductComparisonIN(
        items=[
            ProductItemIN(
                name="Leite UHT",
                brand="marca A",
                price=Decimal("4.50"),
                weight=Decimal("1"),
                unit="l",
            ),
            ProductItemIN(
                name="Leite UHT",
                brand="marca B",
                price=Decimal("3.20"),
                weight=Decimal("900"),
                unit="ml",
            ),
        ]
    )

    result = compare_products(payload)

    assert result.message == "O produto mais vantajoso é Leite UHT (marca B) por R$ 3,20"


def test_incompatible_units_raise_validation_error():
    with pytest.raises(ValueError, match="unidades compatíveis"):
        ProductComparisonIN(
            items=[
                ProductItemIN(
                    name="Produto A",
                    price=Decimal("10.00"),
                    weight=Decimal("500"),
                    unit="g",
                ),
                ProductItemIN(
                    name="Produto B",
                    price=Decimal("5.00"),
                    weight=Decimal("1"),
                    unit="l",
                ),
            ]
        )


def test_compare_coca_cola_pack_is_better():
    payload = ProductComparisonIN(
        items=[
            ProductItemIN(
                name="Refrigerante",
                brand="Coca-Cola",
                price=Decimal("25.00"),
                quantity=Decimal("6"),
                weight=Decimal("250"),
                unit="ml",
            ),
            ProductItemIN(
                name="Refrigerante",
                brand="Coca-Cola",
                price=Decimal("32.00"),
                quantity=Decimal("12"),
                weight=Decimal("200"),
                unit="ml",
            ),
        ]
    )

    result = compare_products(payload)

    assert result.message == "O produto mais vantajoso é Refrigerante (Coca-Cola) por R$ 32,00"
