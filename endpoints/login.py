import logging
from typing import List, Dict
from aiohttp import web
from aiohttp_pydantic import PydanticView


class Login(PydanticView):
    # Get access and refresh tokens
    async def post(self):
        try:
            body = await self.request.json()
        except:
            return web.json_response({"Error": "Wrong data auth data."})

    # Refresh tokens
    async def get(self):
        pass
