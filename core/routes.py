import aiohttp.web as web
from aiohttp.web import Application
from endpoints.tag import Tag
from endpoints.image import Image
# from endpoints.video import Video
from endpoints.tag_group import TagGroup


def setup_routes(app: Application):
    app.router.add_view("/image", Image)
    app.router.add_view("/tag", Tag)
    app.router.add_view("/tag_group", TagGroup)
    return app
