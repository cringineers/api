from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.db_tag_group import insert_tag_group, get_tag_group, get_all
from db.db_tag import get_tags_by_group


class TagGroup(PydanticView):
    # Upload tag group
    async def post(self):
        try:
            body = await self.request.json()
            name = body["name"]
            binary = body["binary"]
            group_id = await insert_tag_group(self.request.app, name, binary)
            return web.json_response({"group_id": group_id}, status=200)
        except Exception as err:
            return web.json_response({"Error": err}, status=500)

    async def get(self, group_id: int):
        try:
            group = await get_tag_group(self.request.app, group_id)
            if group is not None:
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
            else:
                return web.json_response({}, status=404)
        except Exception as err:
            web.json_response({"Error": err}, status=500)


class TagGroups(PydanticView):
    async def get(self):
        try:
            groups = await get_all(self.request.app)
            result = {}
            for g_id, g_name, g_binary, t_id, t_name, t_text, t_latent_space, t_is_fake in groups:
                tag = {"id": t_id, "name": t_name, "text": t_text, "fake": t_is_fake}
                if g_id in result.keys():
                    result[g_id]["tags"].append(tag)
                else:
                    result[g_id] = {"group": {"id": g_id, "name": g_name, "binary": g_binary}, "tags": [tag]}
            return web.json_response(list(result.values()), status=200)
        except Exception as err:
            return web.json_response({"Error": err}, status=500)