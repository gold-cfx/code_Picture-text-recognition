import configparser
import sys

import keyboard as keyboard
from aip import AipOcr
from time import sleep
from PIL import Image, ImageGrab
from functools import reduce


def screenShot():
    if keyboard.wait(hotkey='ctrl + alt + a') == None:
        print('开始截图')
        if keyboard.wait(hotkey='enter') == None:
            print('截图完成')
            sleep(0.1)
            im = ImageGrab.grabclipboard()
            if isinstance(im, Image.Image):
                im.save('Picture.png')
                print('保存成功')
            else:
                print('保存失败，重新截图')


class BaiDuAPI():

    def __init__(self, filepath=None):
        target = configparser.ConfigParser()
        target.read(filepath)
        api_id = target.get('my_message', 'APP_ID')
        api_key = target.get('my_message', 'API_KEY')
        secret_key = target.get('my_message', 'SECRET_KEY')

        self.client = AipOcr(api_id, api_key, secret_key)

    def picture2Text(self, filepath):
        '''根据图像识别文字'''
        image = self.getPictuer(filepath)
        texts = self.client.basicGeneral(image)
        return texts

    @staticmethod
    def getPictuer(filepath):
        with open(filepath, 'rb') as fp:
            return fp.read()


def main():
    for _ in range(sys.maxsize):
        screenShot()
        print('开始解析')
        baiduapi = BaiDuAPI('api.ini')
        texts = baiduapi.picture2Text('Picture.png')
        comtent = reduce(lambda x, y: x + y, [words['words'] for words in texts['words_result']])
        print('解析内容为：',comtent, sep='\n')


if __name__ == '__main__':
    main()
