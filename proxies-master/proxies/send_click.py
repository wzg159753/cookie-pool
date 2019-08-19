# coding:utf-8



import json
import re
import base64
from io import BytesIO
from datetime import datetime


import requests
from PIL import Image
from lxml import etree
from requests.sessions import cookiejar_from_dict

from chaojiying import Chaojiying_Client

class Send_Click(object):
    """
    点触验证码
    """
    def __init__(self):
        cookies = self._get_cookies()
        self.session = requests.Session()
        self.session.cookies = cookiejar_from_dict(cookies) # session设置cookie

    @staticmethod
    def _get_cookies(proxy):
        """
        获取cookie 拼接cookie
        :return:
        """
        cookie = {}
        for i in proxy[:-1].split(";"):
            name = i.split("=")[0]
            print(name)
            value = i.split("=")[1]
            print(value)
            cookie[name] = value
        return cookie

    def get_xpath(self, response, xpath, html=None):
        """
        解析器
        :param response:
        :param xpath:
        :param html:
        :return:
        """
        if html is None:
            html = etree.HTML(response)
            return html.xpath(xpath)
        else:
            return response.xpath(xpath)


    def download(self, url, params=None):
        """
        下载器
        :param url:
        :param params:
        :return:
        """
        return self.session.get(url, params=params)

    def verify(self, response):
        """
        验证是不是点触验证码
        :param response:
        :return:
        """
        title = re.search(r'<title>(.*?)</title>', response)
        return title.group(1) if title else None

    def slice(self, targetImage, bgImage):
        """
        拼接图片验证码
        :param targetImage: 验证图片 点击顺序字符
        :param bgImage: 验证图片  字符
        :return:
        """
        # 打开文件二进制流图片bytes数据
        img = Image.open(BytesIO(base64.urlsafe_b64decode(targetImage)))
        img2 = Image.open(BytesIO(base64.urlsafe_b64decode(bgImage)))

        # new_image 是拼接好的图片
        new_image = Image.new('RGB', (320, 130), 'red')
        new_image.paste(img, (0, 0))
        new_image.paste(img2, (0, 30))

        new_image.show()

        # ===============模拟打码平台=================
        a = {'err_no': 0, 'err_str': 'OK', 'pic_id': '3074318422563200076', 'pic_str': '157,82|189,93|294,75', 'md5': '40c1c57c748b1f6b10a91222c12754d3'}
        # 接入超级鹰打码平台
        chaojiying = Chaojiying_Client("L54555", "Li891004", '90004')
        im = open('images/out.png', 'rb').read()
        # 获取超级鹰返回坐标
        r_json = chaojiying.PostPic(im, 9004)
        print(r_json)
        lis = []
        if r_json['err_str'] == 'OK':
            pic_str = r_json["pic_str"].split('|')

            for pic in pic_str[:]:
                pic_x = pic.split(',')[0]
                pic_y = pic.split(',')[1]
                lis.append({'x': pic_x, 'y': pic_y})
            # 返回坐标列表
            return lis
        else:
            print(r_json['err_str'])
            return lis



    def verify_image(self):
        # 获取图片验证码返回的图片  b64串
        url = "http://antirobot.tianyancha.com/captcha/getCaptcha.json?t={str(int(datetime.now().timestamp() * 1000))}"
        result = self.download(url)  # 获取数据
        data = result.json().get('data')
        targetImage = data.get('targetImage') # 拿到要顺序点击的字符
        bgImage = data.get('bgImage') # 拿到字符图片
        captchaId = data.get('id') # 拿到图片id

        # 拼接图片  函数里面接入打码平台
        lis = self.slice(targetImage, bgImage)

        # 拼接参数  发送验证请求
        params = {
            'captchaId': captchaId,  # 图片唯一id
            'clickLocs': json.dumps(lis),  # 图片坐标
            't': str(int(datetime.now().timestamp() * 1000)) # 当前时间戳
        }
        # 验证成功
        resp = self.download("http://antirobot.tianyancha.com/captcha/checkCaptcha.json", params=params)
        # print(resp.json().get('state'))
        return resp.json().get('state')



    def run(self, proxy):
        # 添加待验证cookie
        self._get_cookies(proxy)
        # 爬接口  如果是正常网页  title不会是  天眼查验证
        url = 'https://www.tianyancha.com/company/3270966165'
        resp = self.download(url)
        # print(resp.text)
        title = self.verify(resp.text)
        print(title)
        if title != '天眼查校验':
            # 如果没有验证码
            pass
        else:
            # 如果是点触验证码
            # 调用验证 接打码平台 返回坐标 [{"x":72,"y":66},{"x":97,"y":32}]  坐标类型list 里面每个字符组成一个字典x,y  依次顺序
            if self.verify_image() == 'ok':
                # 可以继续爬这个接口  url
                # result = self.download(url) # 验证成功后可以继续操作
                # print(result.text)
                return True
            else:
                # 没验证成功  继续验证
                resp = self.verify_image()
                print(resp)


if __name__ == '__main__':
    click = Send_Click()
    # 爬一个接口
    click.run("cookies")

