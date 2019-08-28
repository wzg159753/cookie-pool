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

    def __init__(self, url, cookies2=None, proxies=None, cookies=None):
        self.url = url
        self.proxies = proxies
        # cookies = cookies2 if cookies2 else self._get_cookies()
        self.session = requests.Session()
        self.session.cookies = cookiejar_from_dict(cookies)  # session设置cookie
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'antirobot.tianyancha.com',
            'Cookies': cookies,
            'Referer': 'https://antirobot.tianyancha.com/captcha/verify?return_url={}&rnd='.format(self.url),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'X-CSRFToken': 'null',
            'X-Requested-With': 'XMLHttpRequest',
        }
        # self.session.headers = headers

    @staticmethod
    def _get_cookies():
        """
        获取cookie 拼接cookie
        :return:
        """
        cookie = {}
        with open('cookies.txt', 'r') as f:
            result = json.load(f)

        for c in result:
            name = c.get('name')
            value = c.get('value')
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

    def download(self, url, params=None, proxies=None):
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
        # response_html = etree.HTML(response.text)
        # company_id = response_html.xpath('//div[@class="search-result-single   "]/@data-id')
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

        # new_image.show()
        # new_image.save('captcha.jpg')

        chaojiying = Chaojiying_Client("L54555", "Li891004", '90004')  # 用户中心>>软件ID 生成一个替换 96001
        # im = open('a.jpg', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
        bytes_image = BytesIO()
        new_image.save(bytes_image, format='PNG')
        new_image = bytes_image.getvalue()
        dict_data = chaojiying.PostPic(new_image, 9004)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
        pic_str = dict_data.get('pic_str').split('|')
        print(pic_str)
        lis = []
        if pic_str[0]:
            [lis.append({'x':int(data.split(',')[0]),'y':int(data.split(',')[1])-30}) for data in pic_str]
        # ===============模拟打码平台=================
        # for _ in range(4):
        #     x = int(input('请输入坐标x:'))
        #     if x == 0:
        #         break
        #     y = int(input('请输入坐标y:'))
        #     lis.append({'x': x, 'y': y})

        return lis
        # 返回坐标列表

    def verify_image(self):
        # 获取图片验证码返回的图片  b64串
        # dt = str(int(datetime.now().timestamp() * 1000))
        url = "http://antirobot.tianyancha.com/captcha/getCaptcha.json?t={}&_={}".format(str(int(datetime.now().timestamp() * 1000)), str(int(datetime.now().timestamp() * 1000) - 100))
        result = self.download(url)  # 获取数据
        data = result.json().get('data')
        targetImage = data.get('targetImage')  # 拿到要顺序点击的字符
        bgImage = data.get('bgImage')  # 拿到字符图片
        captchaId = data.get('id')  # 拿到图片id
        print(result.json())
        # 拼接图片  函数里面接入打码平台
        lis = self.slice(targetImage, bgImage)

        # 拼接参数  发送验证请求
        params = {
            'captchaId': captchaId,  # 图片唯一id
            'clickLocs': json.dumps(lis),  # 图片坐标
            't': str(int(datetime.now().timestamp() * 1000)),  # 当前时间戳
        }

        # 验证成功
        # dd = str(int(datetime.now().timestamp() * 1000))
        # url = f'https://antirobot.tianyancha.com/captcha/checkCaptcha.json?captchaId={captchaId}&clickLocs={json.dumps(str(lis))}&t={str(int(datetime.now().timestamp() * 1000))}&_={str(int(datetime.now().timestamp() * 1000) - 100)}'
        resp = self.download("http://antirobot.tianyancha.com/captcha/checkCaptcha.json", params=params)
        print(resp.json(), '*'*10)
        return resp.json().get('state')

    def run(self):
        # 爬接口  如果是正常网页  title不会是  天眼查验证
        resp = self.download(self.url)
        title = self.verify(resp.text)
        print(title, '++++++++++++++++++++++++++++++')
        html = etree.HTML(resp.text)
        user = html.xpath('//span[@class="ni-sp-name"]')
        print(user)
        if user and title != '天眼查校验':
            return 200
            # 继续操作
        else:
            # 如果是点触验证码
            # 调用验证 接打码平台 返回坐标 [{"x":72,"y":66},{"x":97,"y":32}]  坐标类型list 里面每个字符组成一个字典x,y  依次顺序
            if self.verify_image() == 'ok':
                # 可以继续爬这个接口  url
                response = self.download(self.url) # 验证成功后可以继续操作
                html = etree.HTML(response.text)
                result = html.xpath('//span[@class="ni-sp-name"]')
                # //span[@class="ni-sp-name"]
                print(result, '='*10)
                if result:
                    print(response.status_code)
                    return response.status_code
                else:
                    return 503

            else:
                # 没验证成功  继续验证
                # self.run()
                return 503

if __name__ == '__main__':
    url = 'https://www.tianyancha.com/company/3270966165'
    click = Send_Click(url)
    # 爬一个接口
    click.run()
