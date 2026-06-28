from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from schema.comparison_schema import SUPPORTED_UNITS


class PriceType(str, Enum):
    NORMAL = "normal"
    WHOLESALE = "wholesale"


class CartStatus(str, Enum):
    ACTIVE = "active"
    FINALIZED = "finalized"


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, description="Nome do produto")
    brand: str | None = Field(default=None, description="Marca do produto")
    category: str | None = Field(default=None, description="Categoria do produto")


class ProductIN(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, description="Nome do produto")
    brand: str | None = Field(default=None, description="Marca do produto")
    category: str | None = Field(default=None, description="Categoria do produto")


class ProductOUT(ProductBase):
    id: UUID = Field(description="Identificador do produto")


class CartItemBase(BaseModel):
    total_price: Decimal = Field(..., gt=0, description="Preço total pago pelo item")
    quantity: Decimal = Field(
        ...,
        gt=0,
        description="Quantidade por unidade (ex.: 300 para um pacote de 300g)",
    )
    unit: SUPPORTED_UNITS = Field(..., description="Unidade de medida (mg, g, kg, ml, l)")
    purchased_quantity: Decimal = Field(
        default=Decimal("1"),
        gt=0,
        description="Quantidade de unidades compradas",
    )
    price_type: PriceType = Field(
        default=PriceType.NORMAL,
        description="Tipo de preço: normal ou atacado",
    )
    wholesale_min_quantity: Decimal | None = Field(
        default=None,
        gt=0,
        description="Quantidade mínima exigida para preço de atacado",
    )


class CartIN(CartItemBase):
    product_id: UUID | None = Field(
        default=None,
        description="Identificador de um produto já cadastrado",
    )
    product: ProductIN | None = Field(
        default=None,
        description="Dados para cadastrar um novo produto junto com o item",
    )

    @model_validator(mode="after")
    def validate_product_reference(self) -> "CartIN":
        has_product_id = self.product_id is not None
        has_product = self.product is not None

        if has_product_id == has_product:
            raise ValueError(
                "Informe product_id de um produto existente ou product para cadastrar um novo"
            )
        return self

    @model_validator(mode="after")
    def validate_wholesale_rules(self) -> "CartIN":
        if self.price_type == PriceType.WHOLESALE and self.wholesale_min_quantity is None:
            raise ValueError(
                "wholesale_min_quantity é obrigatório quando price_type é wholesale"
            )

        if self.price_type == PriceType.NORMAL and self.wholesale_min_quantity is not None:
            raise ValueError(
                "wholesale_min_quantity só deve ser informado para price_type wholesale"
            )

        return self


class CartItemOUT(CartItemBase):
    id: UUID = Field(description="Identificador do item no carrinho")
    product: ProductOUT = Field(description="Dados do produto vinculado ao item")
    unit_price: Decimal = Field(
        ...,
        gt=0,
        description="Preço por unidade base normalizado (ex.: R$/kg ou R$/l)",
    )


class CartOUT(BaseModel):
    id: UUID = Field(description="Identificador do carrinho")
    status: CartStatus = Field(description="Status do carrinho")
    total_value: Decimal = Field(description="Valor total acumulado dos itens")
    items: list[CartItemOUT] = Field(default_factory=list, description="Produtos do carrinho")


class CartItemUpdate(BaseModel):
    total_price: Decimal | None = Field(default=None, gt=0, description="Preço total pago pelo item")
    quantity: Decimal | None = Field(
        default=None,
        gt=0,
        description="Quantidade por unidade (ex.: 300 para um pacote de 300g)",
    )
    unit: SUPPORTED_UNITS | None = Field(
        default=None,
        description="Unidade de medida (mg, g, kg, ml, l)",
    )
    purchased_quantity: Decimal | None = Field(
        default=None,
        gt=0,
        description="Quantidade de unidades compradas",
    )
    price_type: PriceType | None = Field(
        default=None,
        description="Tipo de preço: normal ou atacado",
    )
    wholesale_min_quantity: Decimal | None = Field(
        default=None,
        gt=0,
        description="Quantidade mínima exigida para preço de atacado",
    )

    @model_validator(mode="after")
    def validate_wholesale_rules(self) -> "CartItemUpdate":
        if self.price_type == PriceType.WHOLESALE and self.wholesale_min_quantity is None:
            raise ValueError(
                "wholesale_min_quantity é obrigatório quando price_type é wholesale"
            )

        if self.price_type == PriceType.NORMAL and self.wholesale_min_quantity is not None:
            raise ValueError(
                "wholesale_min_quantity só deve ser informado para price_type wholesale"
            )

        return self
