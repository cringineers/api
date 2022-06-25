from aiohttp.web import Application
from endpoints.tag import Tag, TagDeleter
from endpoints.image import Image, Images, ImagesSearch, ImageDeleter
from endpoints.tag_group import TagGroup, TagGroups


def setup_routes(app: Application):
    app.router.add_view("/image", Image)
    app.router.add_view("/images", Images)
    app.router.add_view("/images/search", ImagesSearch)
    app.router.add_view("/image/delete", ImageDeleter)
    app.router.add_view("/tag", Tag)
    app.router.add_post("/tag/delete", TagDeleter)
    app.router.add_view("/tag_group", TagGroup)
    app.router.add_view("/tag_groups", TagGroups)
    return app
