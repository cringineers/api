import aiohttp.web as web
from aiohttp.web import Application
from endpoints.tag import Tag
from endpoints.image import Image
from endpoints.video import Video
from endpoints.tag_group import TagGroup


def setup_routes(app: Application):
    app.add_routes([
        web.get("/image", Image),
        web.get("/video", Video),
        web.get("/tag", Tag),
        web.get("/tag_group", TagGroup)
    ])
    return app
