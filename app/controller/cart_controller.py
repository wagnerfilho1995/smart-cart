from uuid import UUID

from fastapi import APIRouter, Depends, status

from database import get_db_pool
from repository.cart_repository import CartRepository
from schema.cart_schema import CartIN, CartOUT
from service import cart_service

cart_controller = APIRouter()


def get_cart_repository() -> CartRepository:
    return CartRepository(get_db_pool())


@cart_controller.get(
    "/current",
    description="Retorna o carrinho ativo com a lista de produtos. Cria um carrinho se não existir.",
    response_model=CartOUT,
    status_code=status.HTTP_200_OK,
)
async def get_current_cart(
    repository: CartRepository = Depends(get_cart_repository),
) -> CartOUT:
    return await cart_service.get_current_cart(repository)


@cart_controller.post(
    "/{cart_id}/add",
    description="Adiciona um produto ao carrinho informado.",
    response_model=CartOUT,
    status_code=status.HTTP_201_CREATED,
)
async def add_product_to_cart(
    cart_id: UUID,
    payload: CartIN,
    repository: CartRepository = Depends(get_cart_repository),
) -> CartOUT:
    return await cart_service.add_item_to_cart(
        repository=repository,
        cart_id=cart_id,
        payload=payload,
    )
