import aiohttp.web as web
from aiohttp.web import Application
from endpoints.login import Login
from endpoints.tag import Tag
from endpoints.image import Image
from endpoints.video import Video


def setup_routes(app: Application):
    app.add_routes([
        web.get("/login", Login),
        web.get("/image", Image),
        web.get("/video", Video),
        web.get("/tag", Tag),
    ])
    return app
