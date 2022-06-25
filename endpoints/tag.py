import json
import requests
from typing import List, Dict
from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.db_tag import *


class Tag(PydanticView):
    async def post(self):
        try:
            body = await self.request.json()
            name = body["name"]
            text = body["text"]
            group_id = body["group_id"]
            binary = body["binary"]
            space = requests.post(f"{self.request.app['worker_host']}/features_tag", json={"text": text}).json()["features"]
            if binary:
                alt_name = "No " + name
                alt_text = "No " + text
                alt_space = requests.post(f"{self.request.app['worker_host']}/features_tag", json={"text": alt_text}).json()["features"]
                alt_tag = await insert_tag(self.request.app, alt_name, alt_text, json.dumps(alt_space), group_id, True)
            tag_id = await insert_tag(self.request.app, name, text, json.dumps(space), group_id, False)
            return web.json_response({"tag_id": tag_id}, status=200)
        except Exception as err:
            return web.json_response({"Error": err}, status=500)

    async def get(self, /, tag_id: int):
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

