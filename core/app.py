import os
import logging
import boto3
import aiohttp_cors
from botocore.client import Config
from aiohttp.web import Application
from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from core.routes import setup_routes


async def create_app():
    if not os.path.exists(find_dotenv(".env")):
        logging.warning("Cant find .env file.")
    load_dotenv()

    app = Application()
    app = setup_routes(app)
    connection_string = f"postgresql+asyncpg://" \
                        f"{os.environ.get('DB_USER')}:%s" % os.environ.get('DB_PASSWORD') + \
                        f"@{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    app['db_engine'] = create_async_engine(
        connection_string,
        pool_size=int(os.environ.get('POOL_SIZE')),
        max_overflow=int(os.environ.get('POOL_OVERFLOW')),
        pool_recycle=int(os.environ.get('POOL_RECYCLE'))
    )
    app["jwt_key"] = os.environ.get('JWT_KEY')
    app["jwt_alg"] = os.environ.get('JWT_ALG')
    app["worker_host"] = os.environ.get('WORKER_HOST')
    app["minio"] = boto3.resource(
        's3',
        endpoint_url=os.environ.get("MINIO_ENDPOINT"),
        aws_access_key_id=os.environ.get("MINIO_ACCESS"),
        aws_secret_access_key=os.environ.get("MINIO_SECRET"),
        verify=False,
        region_name="ru-msk-1"
    )
    app["minio_bucket_name"] = os.environ.get("MINIO_BUCKET")
    app["minio_bucket"] = app["minio"].Bucket(app["minio_bucket_name"])
    return app
