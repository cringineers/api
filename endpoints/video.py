import logging
from typing import List, Dict
from aiohttp import web
from aiohttp_pydantic import PydanticView


class Video(PydanticView):
    # Get access and refresh tokens
    async def post(self):
        pass

    # Refresh tokens
    async def get(self):
        pass
