import requests
import json


class FaceDetect():
    def __init__(self):
        self.ak = "你的百度access_key"
        self.sk = "你的百度secret_key"
        self.token = self.__access_token()

    def __access_token(self):
        url = 'https://aip.baidubce.com/oauth/2.0/token?' \
              'grant_type=client_credentials&client_id={}&client_secret={}'.format(self.ak, self.sk)
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        req = requests.get(url, headers=headers)
        token = json.loads(req.text)["access_token"]
        return token

    def __face_detect(self, pic):
        url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={}".format(self.token)
        params = {
            "image": pic,
            "image_type": "URL",
            "face_field": "age,beauty,expression,gender,face_shape,emotion",
            "max_face_num": "10"
        }
        req = requests.post(url, params=params)
        return req.text

    def __average_beauty(self, data):
        if data["error_code"] == 0:
            average_beauty = []
            for face in data["result"]["face_list"]:
                average_beauty.append(face["beauty"])
            return "{:.4f}".format((sum(average_beauty) / len(average_beauty)))
        return 0

    def __call__(self, url):
        r = self.__face_detect(url)
        data = json.loads(r)
        return self.__average_beauty(data)


if __name__ == '__main__':
    face = FaceDetect()
    print(face("http://aip.bdstatic.com/portal/dist/1558609030912/ai_images/technology/face-detect/intro2.jpg"))
    print(face("https://p3-dy.byteimg.com/aweme/1080x1080/240850005f0f95367bd25.jpeg"))
    print(face("https://p3-dy.byteimg.com/aweme/1080x1080/2401d0006f8298c6b63b7.jpeg"))
    print(face("https://p9-dy.byteimg.com/aweme/1080x1080/1cae800032cb40a6ae150.jpeg"))
