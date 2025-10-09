from app.database.database import pool
import asyncpg


def get_pool() -> asyncpg.Pool:
    if pool is None:
        raise RuntimeError("Database not connected")
    return pool
