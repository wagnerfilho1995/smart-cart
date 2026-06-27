from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator


SUPPORTED_UNITS = Literal["mg", "g", "kg", "ml", "l"]


class ProductItemIN(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do produto")
    brand: str | None = Field(default=None, description="Marca do produto")
    price: Decimal = Field(..., gt=0, description="Preço total do produto")
    quantity: Decimal = Field(default=Decimal("1"), gt=0, description="Quantidade de unidades")
    weight: Decimal = Field(..., gt=0, description="Peso ou volume de cada unidade")
    unit: SUPPORTED_UNITS = Field(..., description="Unidade de medida (mg, g, kg, ml, l)")


class ProductComparisonIN(BaseModel):
    items: list[ProductItemIN] = Field(
        ...,
        min_length=2,
        max_length=2,
        description="Dois produtos para comparação",
    )

    @model_validator(mode="after")
    def validate_same_measure_category(self) -> "ProductComparisonIN":
        units = {item.unit.lower() for item in self.items}
        weight_units = {"mg", "g", "kg"}
        volume_units = {"ml", "l"}

        is_all_weight = units.issubset(weight_units)
        is_all_volume = units.issubset(volume_units)

        if not is_all_weight and not is_all_volume:
            raise ValueError(
                "Os produtos devem usar unidades compatíveis (peso ou volume)"
            )
        return self


class ProductComparisonOUT(BaseModel):
    message: str = Field(description="Mensagem com o produto de melhor custo-benefício")
