from sqlalchemy import text
from aiohttp.web import Application


async def get_tag(app: Application, tag_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select * from tag_system.tags where id = :id
        """)
        tags = await connection.execute(query, {"id": tag_id})
        await connection.commit()
    return tags


async def get_tags_by_group(app: Application, group_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select * from tag_system.tags where group_id = :id
        """)
        tags = await connection.execute(query, {"id": group_id})
        await connection.commit()
    return tags


async def create_tag(app: Application, name, tag_text, latent_space, group_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            insert into tag_system.tags(name, text, latent_space, group_id)
            values(:name, :text, :ls, :group_id)
        """)
        result = await connection.execute(query, {"name": name, "text": tag_text, "ls": latent_space, "group_id": group_id})
        await connection.commit()
    return result.inserted_primary_key


async def update_tag(app: Application, tag_id, name, tag_text):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            update tag_system.tag 
            set name = :name
                text = :text
            where id = :id
        """)
        await connection.execute(query, {"name": name, "text": tag_text, "id": tag_id})
        await connection.commit()
    return tag_id


async def delete_tag(app: Application, tag_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            delete from tag_system.tags where id = :id
        """)
        await connection.execute(query, {"id": tag_id})
        await connection.commit()
    return tag_id