import asyncio

from app.db.postgres import init_db


def main() -> None:
    async def runner() -> None:
        # Ensure schema exists before seeding admin
        await init_db()

    asyncio.run(runner())


if __name__ == "__main__":
    main()
