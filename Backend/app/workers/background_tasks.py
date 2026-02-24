import asyncio


def run_background(task, *args):
    asyncio.create_task(task(*args))
