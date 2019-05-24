import re
import requests


class Short_ID:
    URL = "https://www.iesdouyin.com/share/user/{}"

    codes = {
        "&#xe603;": "0", "&#xe60d;": "0", "&#xe616;": "0",
        "&#xe602;": "1", "&#xe60e;": "1", "&#xe618;": "1",
        "&#xe605;": "2", "&#xe610;": "2", "&#xe617;": "2",
        "&#xe604;": "3", "&#xe611;": "3", "&#xe61a;": "3",
        "&#xe606;": "4", "&#xe60c;": "4", "&#xe619;": "4",
        "&#xe607;": "5", "&#xe60f;": "5", "&#xe61b;": "5",
        "&#xe608;": "6", "&#xe612;": "6", "&#xe61f;": "6",
        "&#xe60a;": "7", "&#xe613;": "7", "&#xe61c;": "7",
        "&#xe60b;": "8", "&#xe614;": "8", "&#xe61d;": "8",
        "&#xe609;": "9", "&#xe615;": "9", "&#xe61e;": "9"
    }

    HEADERS = {
        "Host": "www.iesdouyin.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive"
    }

    def __call__(self, uid):
        parse_id = self.__page_sourse(uid)
        true_id = self.__code_replace(parse_id)
        return true_id

    def __page_sourse(self, uid):
        req = requests.get(Short_ID.URL.format(uid), headers=Short_ID.HEADERS)
        short_id = re.search('''(?<=<p class="shortid">)(.*?)(?=</p>)''', req.text).group()
        parse_id = short_id.replace("抖音ID：     ", "").replace('''<i class="icon iconfont "> ''', "").replace(" </i>",
                                                                                                             "")
        return parse_id

    def __code_replace(self, parse_id):
        for key, value in Short_ID.codes.items():
            if key in parse_id:
                parse_id = parse_id.replace(key, value)
        return parse_id.strip()


if __name__ == '__main__':
    spider = Short_ID()
    print(spider("72221135360"))
