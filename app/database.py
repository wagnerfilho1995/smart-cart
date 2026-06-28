from pathlib import Path

import aiomysql

from config import settings

_pool: aiomysql.Pool | None = None

_SCHEMA_PATH = Path(__file__).parent / "queries" / "init_schema.sql"
_REQUIRED_TABLES = ("carts", "products", "cart_items")


async def init_db_pool() -> None:
    global _pool

    _pool = await aiomysql.create_pool(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        db=settings.MYSQL_DATABASE,
        autocommit=False,
        minsize=1,
        maxsize=10,
    )
    await _init_schema()


async def close_db_pool() -> None:
    global _pool

    if _pool is None:
        return

    _pool.close()
    await _pool.wait_closed()
    _pool = None


def get_db_pool() -> aiomysql.Pool:
    if _pool is None:
        raise RuntimeError("Pool de conexões MySQL não inicializado")
    return _pool


async def _init_schema() -> None:
    async with get_db_pool().acquire() as connection:
        if await _schema_is_initialized(connection):
            return

        schema_sql = _SCHEMA_PATH.read_text(encoding="utf-8")
        statements = [statement.strip() for statement in schema_sql.split(";") if statement.strip()]

        async with connection.cursor() as cursor:
            for statement in statements:
                await cursor.execute(statement)
        await connection.commit()


async def _schema_is_initialized(connection: aiomysql.Connection) -> bool:
    placeholders = ", ".join(["%s"] * len(_REQUIRED_TABLES))
    query = f"""
        SELECT COUNT(*) AS table_count
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s
          AND TABLE_NAME IN ({placeholders})
    """

    async with connection.cursor() as cursor:
        await cursor.execute(query, (settings.MYSQL_DATABASE, *_REQUIRED_TABLES))
        row = await cursor.fetchone()

    return row is not None and row[0] == len(_REQUIRED_TABLES)
