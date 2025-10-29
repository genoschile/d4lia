import asyncio
from app.database.database import connect_to_db, close_db_connection, execute_sql_file


async def main():
    pool = await connect_to_db()

    await execute_sql_file("app/queries/init.sql")

    await close_db_connection(pool)


if __name__ == "__main__":
    asyncio.run(main())
