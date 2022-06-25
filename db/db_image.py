import json
from aiohttp.web import Application
from sqlalchemy import text


__IMAGE_ID__ = 1
__VIDEO_ID__ = 2


async def insert_image(app: Application, name, latent_space):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            insert into tag_system.objects(name, source_path, type, latent_space) values(:name, :name, :type, :ls)
            returning id
        """)
        result = await connection.execute(query, {"name": name, "type": __IMAGE_ID__, "ls": json.dumps(latent_space)})
        await connection.commit()
    return result.fetchone()[0]


async def add_tags(app: Application, image_id, tag_ids):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            insert into tag_system.object_tags(object_id, tag_id) values(:obj, :tag)
        """)
        await connection.execute_many(query, [{"obj": image_id, "tag": tag_id} for tag_id in tag_ids])
        await connection.commit()
