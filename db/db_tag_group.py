from sqlalchemy import text
from aiohttp.web import Application


async def get_all(app: Application):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select g.id, g.name, g.binary, t.id, t.name, t.text, t.latent_space, t.is_fake 
            from tag_system.tag_group as g left join tag_system.tags as t on t.group_id = g.id
        """)
        group = await connection.execute(query)
        await connection.commit()
    return group.fetchall()


async def insert_tag_group(app: Application, name, binary):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            insert into tag_system.tag_group("name", "binary") values(:name, :binary) returning id
        """)
        result = await connection.execute(query, {"name": name, "binary": binary})
        await connection.commit()
    return result.fetchone()[0]


async def get_tag_group(app: Application, group_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            select * from tag_system.tag_group where id = :id
        """)
        group = await connection.execute(query, {"id": group_id})
        await connection.commit()
    return group.fetchone()


async def create_tag_group(app: Application, name, binary):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            insert into tag_system.tag_group(name, binary) values(:name, :bin)
        """)
        result = await connection.execute(query, {"name": name, "bin": binary})
        await connection.commit()
    return result.inserted_primary_key


async def delete_tag_group(app: Application, group_id):
    engine = app["db_engine"]
    async with engine.connect() as connection:
        query = text("""
            delete from tag_system.tag_group where id = :id
        """)
        await connection.execute(query, {"id": group_id})
        await connection.commit()
    return group_id
