import time
from functools import reduce
from threading import Thread

from appium import webdriver

from addons.fans import Fans

AIM_ID = "kriswu_1106"  # 要分析的抖音号

addons = [
    Fans(),
]


# appium session初始化

def init_device():
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['udid'] = "your device"
    desired_caps['deviceName'] = "devices name"
    desired_caps['platformVersion'] = "Android Version"
    desired_caps['appPackage'] = 'com.ss.android.ugc.aweme'
    desired_caps['appActivity'] = 'com.ss.android.ugc.aweme.main.MainActivity'
    desired_caps["unicodeKeyboard"] = True
    desired_caps["resetKeyboard"] = True
    desired_caps["noReset"] = True
    desired_caps["newCommandTimeout"] = 600
    device = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    device.implicitly_wait(3)
    return device


def move_to_fans(device, short_id):
    # 进入搜索页面搜索抖音号并进入粉丝页面
    device.find_element_by_id("com.ss.android.ugc.aweme:id/au1").click()
    device.find_element_by_id("com.ss.android.ugc.aweme:id/a86").send_keys(short_id)
    device.find_element_by_id("com.ss.android.ugc.aweme:id/d5h").click()
    device.find_elements_by_id("com.ss.android.ugc.aweme:id/cwm")[0].click()
    device.find_element_by_id("com.ss.android.ugc.aweme:id/adf").click()


def fans_cycle(device):
    fans_done = []
    while True:
        elements = device.find_elements_by_id("com.ss.android.ugc.aweme:id/d9x")
        all_fans = [x.text for x in elements]
        if reduce(lambda x, y: x and y, [(x in fans_done) for x in all_fans]) and fans_done:
            print("遍历结束, 将会终止session")
            break
        for element in elements:
            if element.text not in fans_done:
                element.click()
                time.sleep(2)
                device.press_keycode("4")
                time.sleep(2)
                fans_done.append(element.text)
        device.swipe(600, 1600, 600, 900, duration=1000)
        if len(fans_done) > 30:
            fans_done = fans_done[10:]


def begin():
    device = init_device()
    move_to_fans(device, AIM_ID)
    fans_cycle(device)
    device.quit()


thread = Thread(target=begin)
thread.start()
