from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from fastapi import HTTPException, status

from repository.cart_repository import CartRepository
from schema.cart_schema import (
    CartIN,
    CartItemOUT,
    CartOUT,
    CartStatus,
    PriceType,
    ProductOUT,
)
from utils.unit_normalizer import normalize_weight


def _calculate_unit_price(payload: CartIN) -> Decimal:
    total_amount = payload.quantity * payload.purchased_quantity
    normalized_amount, _, _ = normalize_weight(weight=total_amount, unit=payload.unit)
    return (payload.total_price / normalized_amount).quantize(
        Decimal("0.0001"),
        rounding=ROUND_HALF_UP,
    )


def _map_cart_item_row(row: dict) -> CartItemOUT:
    return CartItemOUT(
        id=UUID(row["id"]),
        total_price=row["total_price"],
        quantity=row["quantity"],
        unit=row["unit"],
        purchased_quantity=row["purchased_quantity"],
        price_type=PriceType(row["price_type"]),
        wholesale_min_quantity=row["wholesale_min_quantity"],
        unit_price=row["unit_price"],
        product=ProductOUT(
            id=UUID(row["product_id"]),
            name=row["product_name"],
            brand=row["product_brand"],
            category=row["product_category"],
        ),
    )


def _map_cart_to_out(*, cart: dict, items: list[dict]) -> CartOUT:
    return CartOUT(
        id=UUID(cart["id"]),
        status=CartStatus(cart["status"]),
        total_value=cart["total_value"],
        items=[_map_cart_item_row(item) for item in items],
    )


async def get_current_cart(repository: CartRepository) -> CartOUT:
    cart = await repository.get_active_cart()
    if cart is None:
        cart = await repository.create_active_cart()

    items = await repository.get_cart_items(UUID(cart["id"]))
    return _map_cart_to_out(cart=cart, items=items)


async def add_item_to_cart(
    *,
    repository: CartRepository,
    cart_id: UUID,
    payload: CartIN,
) -> CartOUT:
    cart = await repository.get_cart_by_id(cart_id)
    if cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carrinho não encontrado",
        )

    if cart["status"] != CartStatus.ACTIVE.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Carrinho não está ativo",
        )

    if payload.product_id is not None:
        product = await repository.get_product_by_id(payload.product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Produto não encontrado",
            )
        product_id = payload.product_id
    else:
        product = await repository.create_product(payload.product)
        product_id = UUID(product["id"])

    unit_price = _calculate_unit_price(payload)
    await repository.add_cart_item(
        cart_id=cart_id,
        product_id=product_id,
        payload=payload,
        unit_price=unit_price,
    )

    updated_cart = await repository.get_cart_by_id(cart_id)
    if updated_cart is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao recuperar carrinho atualizado",
        )

    items = await repository.get_cart_items(cart_id)
    return _map_cart_to_out(cart=updated_cart, items=items)
