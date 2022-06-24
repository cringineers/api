import logging
from typing import List, Dict
from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.db_tag import *


class Tag(PydanticView):
    async def post(self, method: str, tag_id: int = None, name: str = None, tag_text: str = None, group_id: int = None):
        try:
            status = 200
            # TODO: Add realization
            if method == "create":
                result_id = -1
                pass
            elif method == "update":
                result_id = await update_tag(self.request.app, tag_id, name, tag_text)
            elif method == "delete":
                result_id = await delete_tag(self.request.app, tag_id)
            else:
                return web.json_response({"Forbidden move": method}, status=status)
            return web.json_response({"group_id": result_id}, status=400)
        except Exception as err:
            return web.json_response({"Error": err}, status=500)

    async def get(self, tag_id: int):
        try:
            tag = await get_tag(self.request.app, tag_id)
            return web.json_response({
                "id": tag["id"],
                "name": tag["name"],
                "text": tag["text"],
                "latent_space": tag["latent_space"]
            }, status=200)
        except Exception as err:
            web.json_response({"Error": err}, status=500)

