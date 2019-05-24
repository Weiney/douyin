import mitmproxy.http
import json
from api.baidu import FaceDetect
from lib.shortid import Short_ID

face = FaceDetect()
spider_id = Short_ID()


class Fans():
    def response(self, flow: mitmproxy.http.flow):
        if "aweme/v1/user/?user_id" in flow.request.url:
            user = json.loads(flow.response.text)["user"]
            short_id = user["short_id"]
            nickname = user['nickname']
            uid = user["uid"]
            avatar = user["avatar_larger"]["url_list"][0]
            beauty = face(avatar)
            short_id = spider_id(uid) if short_id == "0" else short_id
            data = {
                "short_id": short_id,
                "nickname": nickname,
                "uid": uid,
                "beauty": beauty
            }
            print(data)
