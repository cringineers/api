import requests
import json
import db.minio as minio
from typing import List
from zlib import decompress
from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.db_image import *
from db.db_tag_group import get_all


class Image(PydanticView):
    # Upload image
    async def post(self, /, name: str, *, authorization: str, content_type: str = "image/jpeg"):
        try:
            image_compressed = await self.request.read()
            image = decompress(image_compressed)
            prediction = requests.post(f"{self.request.app['worker_host']}/features_image", data=image_compressed).json()["features"]
            minio.upload_image(self.request.app, image, name, content_type)
            image_id = await insert_image(self.request.app, name, prediction)
            groups = await get_all(self.request.app)
            groups_json = {}
            for g_id, g_name, g_binary, t_id, t_name, t_text, t_latent_space, t_is_fake  in groups:
                tag_dict = {"id": t_id, "name": t_name, "latent_space": json.loads(t_latent_space), "fake": t_is_fake}
                if g_id not in groups_json:
                    groups_json[g_id] = {"id": g_id, "name": g_name, "binary": g_binary, "tags": [tag_dict]}
                else:
                    groups_json[g_id]["tags"].append(tag_dict)
            img_ls = [{"id": image_id, "latent_space": prediction}]
            prediction = requests.post(f"{self.request.app['worker_host']}/predict_image", json={
                "images": img_ls,
                "tag_groups": list(groups_json.values())
            }).json()

            result_tags = []
            for group in groups_json.values():
                g_id, g_binary = group["id"], group["binary"]
                t_id = prediction[str(g_id)][0]["tag_id"]
                tag = [x for x in groups_json[g_id]["tags"] if x["id"] == t_id][0]
                if not g_binary or (g_binary and not tag["fake"]):
                    result_tags.append(t_id)

            await add_tags(self.request.app, image_id, result_tags)
            return web.json_response({"image_id": image_id}, status=200)
        except Exception as err:
            return web.json_response({"error": "Invalid token"}, status=401)

    # Refresh tokens
    async def get(self, /, image_id: int):
        try:
            image = await get_image(self.request.app, image_id)
            if image is not None:
                tag_ids = await get_image_tags(self.request.app, image_id)
                return web.json_response({
                    "id": image_id,
                    "name": image["name"],
                    "source_path": image["source_path"],
                    "tags": [{"id": tag["tag_id"], "name": tag["name"]} for tag in tag_ids]
                }, status=200)
            return web.json_response({}, status=404)
        except Exception as err:
            return web.json_response({"error": "Invalid token"}, status=400)


class Images(PydanticView):
    async def get(self, /, page: int, size: int):
        try:
            count = await get_image_count(self.request.app)
            images = await get_images_page(self.request.app, page, size)
            result = []
            for i_id, i_name, i_source in images:
                tag_ids = await get_image_tags(self.request.app, i_id)
                result.append({
                    "id": i_id,
                    "name": i_name,
                    "source_path": i_source,
                    "tags": [{"id": tag["tag_id"], "name": tag["name"]} for tag in tag_ids]
                })
            return web.json_response({"images": result, "count": count}, status=200)
        except Exception as err:
            return web.json_response({"error": "Invalid token"}, status=400)


class ImagesSearch(PydanticView):
    async def get(self, /, page: int, size: int, tags: List[int]):
        try:
            image_ids = await get_images_search(self.request.app, tags)
            count = len(image_ids)
            image_ids = image_ids[page * size:(page + 1) * size]
            images = await get_images_by_ids(self.request.app, image_ids)
            result = []
            for i_id, i_name, i_source in images:
                tag_ids = await get_image_tags(self.request.app, i_id)
                result.append({
                    "id": i_id,
                    "name": i_name,
                    "source_path": i_source,
                    "tags": [{"id": tag["tag_id"], "name": tag["name"]} for tag in tag_ids]
                })
            return web.json_response({"images": result, "count": count}, status=200)
        except Exception as err:
            raise err
            return web.json_response({"error": "Invalid token"}, status=400)


class ImageDeleter(PydanticView):
    async def post(self, /, image_id: int):
        try:
            image = await get_image(self.request.app, image_id)
            minio.delete_image(self.request.app, image["source_path"])
            await delete_image(self.request.app, image_id)
            return web.json_response({"status": "Done"}, status=200)
        except Exception as err:
            return web.json_response({"error": "Invalid token"}, status=400)
