from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.db_tag_group import insert_tag_group, get_tag_group
from db.db_tag import get_tags_by_group


class TagGroup(PydanticView):
    async def post(self):
        try:
            body = await self.request.json()
            name = body["name"]
            binary = body["binary"]
            group_id = await insert_tag_group(self.request.app, name, binary)
            return web.json_response({"group_id": group_id}, status=400)
        except Exception as err:
            return web.json_response({"Error": err}, status=500)

    async def get(self, group_id: int):
        try:
            group = await get_tag_group(self.request.app, group_id)
            tags = await get_tags_by_group(self.request.app, group_id)
            return web.json_response({
                "group": {
                    "id": group_id,
                    "name": group["name"],
                    "binary": group["binary"],
                },
                "tags": [{"id": tag["id"],
                          "name": tag["name"],
                          "text": tag["text"],
                          "latent_space": tag["latent_space"]
                          } for tag in tags]
            }, status=200)
        except Exception as err:
            web.json_response({"Error": err}, status=500)
