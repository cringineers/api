import os
from aiohttp.web import Application
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from core.routes import setup_routes


async def create_app():
    if not os.path.exists(find_dotenv(".env")):
        raise FileNotFoundError("Cant find .env file.")
    load_dotenv()

    app = Application()
    connection_string = f"postgresql+asyncpg://" \
                        f"{os.environ.get('DB_USER')}:%s" % os.environ.get('DB_PASSWORD') + \
                        f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    app['db_engine'] = create_async_engine(
        connection_string,
        pool_size=int(os.environ.get('POOL_SIZE')),
        max_overflow=int(os.environ.get('POOL_OVERFLOW')),
        pool_recycle=int(os.environ.get('POOL_RECYCLE'))
    )
    app = setup_routes(app)
    return app
