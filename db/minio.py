import io
from aiohttp.web import Application


def upload_image(app: Application, image, name, content_type):
    bucket = app["minio_bucket"]
    bucket.put_object(Body=image, Key=name, ContentType=content_type)
