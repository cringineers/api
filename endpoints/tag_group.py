from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.db_tag_group import *
from db.db_tag import get_tags_by_group


class TagGroup(PydanticView):
    async def post(self, method: str, group_id: int = None, name: str = None, text: str = None):
        try:
            status = 200
            if method == "create":
                result_id, status = await create_tag_group(self.request.app, name, binary), 201
            elif method == "update":
                result_id = await update_tag_group(self.request.app, group_id, name)
            elif method == "delete":
                result_id = await delete_tag_group(self.request.app, group_id)
            else:
                return web.json_response({"Forbidden move": method}, status=status)
            return web.json_response({"group_id": result_id}, status=400)
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
