from decimal import Decimal
from uuid import UUID, uuid4

import aiomysql

from schema.cart_schema import CartIN, ProductIN


class CartRepository:
    def __init__(self, pool: aiomysql.Pool) -> None:
        self._pool = pool

    async def get_active_cart(self) -> dict | None:
        query = """
            SELECT id, status, total_value, supermarket, created_at, finalized_at
            FROM carts
            WHERE status = 'active'
            ORDER BY created_at DESC
            LIMIT 1
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query)
                return await cursor.fetchone()

    async def get_cart_by_id(self, cart_id: UUID) -> dict | None:
        query = """
            SELECT id, status, total_value, supermarket, created_at, finalized_at
            FROM carts
            WHERE id = %s
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (str(cart_id),))
                return await cursor.fetchone()

    async def create_active_cart(self) -> dict:
        cart_id = str(uuid4())
        query = """
            INSERT INTO carts (id, status, total_value)
            VALUES (%s, 'active', 0)
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (cart_id,))
            await connection.commit()

        cart = await self.get_cart_by_id(UUID(cart_id))
        if cart is None:
            raise RuntimeError("Falha ao criar carrinho ativo")
        return cart

    async def get_product_by_id(self, product_id: UUID) -> dict | None:
        query = """
            SELECT id, name, brand, category
            FROM products
            WHERE id = %s
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (str(product_id),))
                return await cursor.fetchone()

    async def create_product(self, product: ProductIN) -> dict:
        product_id = str(uuid4())
        query = """
            INSERT INTO products (id, name, brand, category)
            VALUES (%s, %s, %s, %s)
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    query,
                    (product_id, product.name, product.brand, product.category),
                )
            await connection.commit()

        created_product = await self.get_product_by_id(UUID(product_id))
        if created_product is None:
            raise RuntimeError("Falha ao criar produto")
        return created_product

    async def add_cart_item(
        self,
        *,
        cart_id: UUID,
        product_id: UUID,
        payload: CartIN,
        unit_price: Decimal,
    ) -> None:
        item_id = str(uuid4())
        query = """
            INSERT INTO cart_items (
                id,
                cart_id,
                product_id,
                total_price,
                quantity,
                unit,
                purchased_quantity,
                price_type,
                wholesale_min_quantity,
                unit_price
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    query,
                    (
                        item_id,
                        str(cart_id),
                        str(product_id),
                        payload.total_price,
                        payload.quantity,
                        payload.unit,
                        payload.purchased_quantity,
                        payload.price_type.value,
                        payload.wholesale_min_quantity,
                        unit_price,
                    ),
                )
                await cursor.execute(
                    """
                    UPDATE carts
                    SET total_value = (
                        SELECT COALESCE(SUM(total_price), 0)
                        FROM cart_items
                        WHERE cart_id = %s
                    )
                    WHERE id = %s
                    """,
                    (str(cart_id), str(cart_id)),
                )
            await connection.commit()

    async def get_cart_items(self, cart_id: UUID) -> list[dict]:
        query = """
            SELECT
                ci.id,
                ci.total_price,
                ci.quantity,
                ci.unit,
                ci.purchased_quantity,
                ci.price_type,
                ci.wholesale_min_quantity,
                ci.unit_price,
                p.id AS product_id,
                p.name AS product_name,
                p.brand AS product_brand,
                p.category AS product_category
            FROM cart_items ci
            INNER JOIN products p ON p.id = ci.product_id
            WHERE ci.cart_id = %s
            ORDER BY ci.created_at ASC
        """

        async with self._pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, (str(cart_id),))
                rows = await cursor.fetchall()
                return list(rows)
