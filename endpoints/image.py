import requests
import json
import jwt
from aiohttp import web
from aiohttp_pydantic import PydanticView
from db.minio import upload_image
from db.db_image import insert_image, add_tags
from db.db_tag_group import get_all


class Image(PydanticView):
    # Upload image
    async def post(self, /, name: str, *, authorization: str, content_type: str = "image/jpeg"):
        try:
            '''
            _ = jwt.decode(authorization.split()[1],
                           key=self.request.app["jwt_key"],
                           algorithm=self.request.app["jwt_alg"])
            '''
            image = await self.request.read()
            prediction = requests.post(f"{self.request.app['worker_host']}/features_image", data=image).json()["features"]
            upload_image(self.request.app, image, name, content_type)
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
    async def get(self):
        pass
