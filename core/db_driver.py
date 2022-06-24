from sqlalchemy import text
from aiohttp.web import Application


# OBJECT CRUD
async def get_object(app: Application, id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select * from tag_system.object
            where id = :id
        """)
        data = await connection.execute(query, {"id": id})
        await connection.commit()
    return data


async def upload_object(app: Application, object, type, name):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text()
        # data = await connection.execute(query)
        # await connection.commit()
    raise NotImplementedError()


async def update_object(app: Application, id, tag_ids, name):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            update tag_system.objects set name = :name where id = :id
        """)
        await connection.execute(query, {"id": id, "name": name})
        # TODO: UPDATE TAGS
        await connection.commit()


async def delete_object(app: Application, id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            delete from tag_system.objects where id = :id
        """)
        await connection.execute(query, {"id": id})
        await connection.commit()


# TAGS
async def create_tag(app: Application, text, latent_space):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            insert into tag_system.tags(text, latent_space) values(:text, :space)
        """)
        await connection.execute(query, {"text": text, "space": latent_space})
        await connection.commit()


async def delete_tag(app: Application, id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            delete from tag_system.tags
            where id = :id
        """)
        await connection.execute(query, {"id": id})
        await connection.commit()


