import logging
import asyncio
import argparse
import uvloop
from aiohttp.web import run_app
from core.app import create_app


logging_level = logging.INFO


async def main():
    app = await create_app()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    logging.info(f"Server started")
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port')
    args = parser.parse_args()
    run_app(main(), port=args.port)
