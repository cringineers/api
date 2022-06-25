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
        await connection.execute(query, [{"obj": image_id, "tag": tag_id} for tag_id in tag_ids])
        await connection.commit()


async def get_image(app: Application, image_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select id, name, source_path
            from tag_system.objects
            where id = :id
        """)
        result = await connection.execute(query, {"id": image_id})
        await connection.commit()
    return result.fetchone()


async def get_image_tags(app: Application, image_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select tag_id, name
            from tag_system.object_tags left join tag_system.tags on tag_id = id
            where object_id = :id
        """)
        result = await connection.execute(query, {"id": image_id})
        await connection.commit()
    return result.fetchall()


# TODO: FIX PAGINATION
async def get_images_page(app: Application, page, size):
    engine = app["db_engine"]
    limit = size * (page + 1)
    offset = size * page
    async with engine.connect() as connection:
        query = text("""
            select id, name, source_path 
            from tag_system.objects 
            order by id
            limit :limit offset :offset
        """)
        result = await connection.execute(query, {"limit": limit, "offset": offset})
        await connection.commit()
    return result.fetchall()


async def get_image_count(app: Application):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select count(*)
            from tag_system.objects 
        """)
        result = await connection.execute(query)
        await connection.commit()
    return result.fetchone()[0]
