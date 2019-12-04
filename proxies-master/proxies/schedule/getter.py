# -*-coding:utf-8 -*-
from schedule.db import RedisClient, POOL_UPPER_THRESHLD

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import re, time
from PIL import Image
from time import sleep
import random
import numpy as np

from schedule.send_click import Send_Click
from util.configtion import logger


class ProxyMetaClass(type):
    """元类，初始化类时记录所有以crawl_开头的方法"""
    def __new__(mcs, name, bases, attrs):
        count = 0
        attrs['CrawlFunc'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['CrawlFunc'].append(k)
                count += 1
        attrs['CrawlFuncCount'] = count
        return type.__new__(mcs, name, bases, attrs)


class Crawler(metaclass=ProxyMetaClass):

    # def get_proxies(self, cookie):
    #     """执行指定方法来获取cookie"""
    #     proxies = []
    #     proxies.append(cookie)
    #     return proxies
    # 登录
    def login(self, username, password):
        # 定义为全局变量，方便其他模块使用
        global url, browser, wait
        # 登录界面的url
        url = 'https://www.tianyancha.com/login'
        # 实例化一个chrome浏览器
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        # chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument("--start-maximized")
        # chrome_options.add_extension()
        # 无头
        # ua = UserAgent()
        # chrome_options.add_argument('user-agent={}'.format(ua.random))
        # chrome_options.add_argument('--disable-gpu')
        browser = webdriver.Chrome()
        browser.set_window_size(1920, 1080)
        # 打开登录页面
        browser.get(url)
        sleep(1)

        # 设置等待超时
        wait = WebDriverWait(browser, 20)
        # 获取用户名输入框
        browser.find_element_by_xpath('.//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div/div[2]').click()
        # 输入用户名
        browser.find_element_by_xpath('.//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[2]/div[2]/input').send_keys(username)
        # 输入密码
        browser.find_element_by_xpath('.//*[@id="web-content"]/div/div[2]/div/div[2]/div/div[3]/div[2]/div[3]/input').send_keys(password)
        # 点击登陆
        browser.find_element_by_xpath(".//*[@id='web-content']/div/div[2]/div/div[2]/div/div[3]/div[2]/div[5]").click()
        sleep(1)

    # 获取图片信息
    def get_image_info(self, img):
        '''
        :param img: (Str)想要获取的图片类型：带缺口、原始
        :return: 该图片(Image)、位置信息(List)
        '''
        # 将网页源码转化为能被解析的lxml格式
        soup = BeautifulSoup(browser.page_source, 'lxml')
        # 获取验证图片的所有组成片标签
        imgs = soup.find_all('div', {'class': 'gt_cut_'+img+'_slice'})
        # 用正则提取缺口的小图片的url，并替换后缀
        try:
            img_url = re.findall('url\(\"(.*)\"\);', imgs[0].get('style'))[0].replace('webp', 'jpg')
        except Exception as e:
            img_url = "https://static.geetest.com/pictures/gt/fc064fc73/bg/3a34c76c4.jpg"
        # 使用urlretrieve()方法根据url下载缺口图片对象
        urlretrieve(url=img_url, filename=img+'.jpg')
        # 生成缺口图片对象
        image = Image.open(img+'.jpg')
        # 获取组成他们的小图片的位置信息
        position = self.get_position(imgs)
        # 返回图片对象及其位置信息
        return image, position

    # 获取小图片位置
    def get_position(self, img):
        '''
        :param img: (List)存放多个小图片的标签
        :return: (List)每个小图片的位置信息
        '''

        img_position = []
        for small_img in img:
            position = {}
            # 获取每个小图片的横坐标
            position['x'] = int(re.findall('background-position: (.*)px (.*)px;', small_img.get('style'))[0][0])
            # 获取每个小图片的纵坐标
            position['y'] = int(re.findall('background-position: (.*)px (.*)px;', small_img.get('style'))[0][1])
            img_position.append(position)
        return img_position

    # 裁剪图片
    def Corp(self, image, position):
        '''
        :param image:(Image)被裁剪的图片
        :param position: (List)该图片的位置信息
        :return: (List)存放裁剪后的每个图片信息
        '''
        # 第一行图片信息
        first_line_img = []
        # 第二行图片信息
        second_line_img = []
        for pos in position:
            if pos['y'] == -58:
                first_line_img.append(image.crop((abs(pos['x']), 58, abs(pos['x']) + 10, 116)))
            if pos['y'] == 0:
                second_line_img.append(image.crop((abs(pos['x']), 0, abs(pos['x']) + 10, 58)))
        return first_line_img, second_line_img

    # 拼接大图
    def put_imgs_together(self, first_line_img, second_line_img, img_name):
        '''
        :param first_line_img: (List)第一行图片位置信息
        :param second_line_img: (List)第二行图片信息
        :return: (Image)拼接后的正确顺序的图片
        '''

        # 新建一个图片，new()第一个参数是颜色模式，第二个是图片尺寸
        image = Image.new('RGB', (260,116))
        # 初始化偏移量为0
        offset = 0
        # 拼接第一行
        for img in first_line_img:
            # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
            image.paste(img, (offset, 0))
            # 偏移量对应增加移动到下一个图片位置,size[0]表示图片宽度
            offset += img.size[0]
        # 偏移量重置为0
        x_offset = 0
        # 拼接第二行
        for img in second_line_img:
            # past()方法进行粘贴，第一个参数是被粘对象，第二个是粘贴位置
            image.paste(img, (x_offset, 58))
            # 偏移量对应增加移动到下一个图片位置，size[0]表示图片宽度
            x_offset += img.size[0]
        # 保存图片
        image.save(img_name)
        # 返回图片对象
        return image

    # 判断像素是否相同
    def is_pixel_equal(self, bg_image, fullbg_image, x, y):
        """
        :param bg_image: (Image)缺口图片
        :param fullbg_image: (Image)完整图片
        :param x: (Int)位置x
        :param y: (Int)位置y
        :return: (Boolean)像素是否相同
        """

        # 获取缺口图片的像素点(按照RGB格式)
        bg_pixel = bg_image.load()[x, y]
        # 获取完整图片的像素点(按照RGB格式)
        fullbg_pixel = fullbg_image.load()[x, y]
        # 设置一个判定值，像素值之差超过判定值则认为该像素不相同
        threshold = 60
        # 判断像素的各个颜色之差，abs()用于取绝对值
        if (abs(bg_pixel[0] - fullbg_pixel[0] < threshold) and abs(bg_pixel[1] - fullbg_pixel[1] < threshold) and abs(bg_pixel[2] - fullbg_pixel[2] < threshold)):
            # 如果差值在判断值之内，返回是相同像素
            return True

        else:
            # 如果差值在判断值之外，返回不是相同像素
            return False

    # 计算滑块移动距离
    def get_distance(self, bg_image, fullbg_image):
        '''
        :param bg_image: (Image)缺口图片
        :param fullbg_image: (Image)完整图片
        :return: (Int)缺口离滑块的距离
        '''
        # 滑块的初始位置
        distance = 57
        # 遍历像素点横坐标
        for i in range(distance, fullbg_image.size[0]):
            # 遍历像素点纵坐标
            for j in range(fullbg_image.size[1]):
                # 如果不是相同像素
                if not self.is_pixel_equal(fullbg_image, bg_image, i, j):
                    # 返回此时横轴坐标就是滑块需要移动的距离
                    return i

    def ease_out_quad(self, x):
        return 1 - (1 - x) * (1 - x)

    def ease_out_quart(self, x):
        return 1 - pow(1 - x, 4)

    def ease_out_expo(self, x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    #构造滑动轨迹
    def get_trace(self, distance, seconds, ease_func):
        '''
        :param distance: (Int)缺口离滑块的距离
        :return: (List)移动轨迹
        '''
        distance += 10
        tracks = [0]
        offsets = [0]
        a = 0
        for t in np.arange(0.0, seconds, 0.2):
            # ease = globals()[ease_func]
            if t < seconds*(2/5):
                random_num = random.choice ([0.1, 0.1, 0.1, 0.2, 0.2])
                a += random_num
                # print(a)
                offset = round(self.ease_out_expo(a / seconds) * distance)
                tracks.append(offset - offsets[-1])
                offsets.append(offset)
            else:
                # print(t)
                offset = round(self.ease_out_expo(t / seconds) * distance)
                tracks.append(offset - offsets[-1])
                offsets.append(offset)
        for i in range(4):
           tracks.append(-random.randint(1,3))
        for i in range(4):
           tracks.append(-random.randint(1,3))

        return tracks

    # 模拟拖动
    def move_to_gap(self, trace):

        # 得到滑块标签
        slider = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gt_slider_knob')))
        # 使用click_and_hold()方法悬停在滑块上，perform()方法用于执行
        ActionChains(browser).click_and_hold(slider).perform()
        for x in trace:
            # 使用move_by_offset()方法拖动滑块，perform()方法用于执行
            ActionChains(browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # 模拟人类对准时间
        sleep(1)
        # 释放滑块
        ActionChains(browser).release().perform()

    def click_locxy(self, dr, x, y, left_click=True):
        '''
        dr:浏览器
        x:页面x坐标
        y:页面y坐标
        left_click:True为鼠标左键点击，否则为右键点击
        '''
        if left_click:
            time.sleep(2)
            ActionChains(dr).move_by_offset(x, y).click().perform()
        else:
            ActionChains(dr).move_by_offset(x, y).context_click().perform()
        ActionChains(dr).move_by_offset(-x, -y).perform()

    # 主程序
    def crawl_main(self, username, password):
        # username = "15531241572" #'13375358581'
        # password = "Li891004" #'uniccc666'
        # 初始化
        # 登录
        try:
            self.login(username, password)
            # 获取缺口图片及其位置信息
            bg, bg_position = self.get_image_info('bg')
            # 获取完整图片及其位置信息
            fullbg, fullbg_position = self.get_image_info('fullbg')
            # 将混乱的缺口图片裁剪成小图，获取两行的位置信息
            bg_first_line_img, bg_second_line_img = self.Corp(bg, bg_position)
            # 将混乱的完整图片裁剪成小图，获取两行的位置信息
            fullbg_first_line_img, fullbg_second_line_img = self.Corp(fullbg, fullbg_position)
            # 根据两行图片信息拼接出缺口图片正确排列的图片
            bg_image = self.put_imgs_together(bg_first_line_img, bg_second_line_img, 'bg.jpg')
            # 根据两行图片信息拼接出完整图片正确排列的图片
            fullbg_image = self.put_imgs_together(fullbg_first_line_img, fullbg_second_line_img, 'fullbg.jpg')
            # 计算滑块移动距离
            distance = self.get_distance(bg_image, fullbg_image)
            # 计算移动轨迹
            trace = self.get_trace(distance, 12, 'ease_out_expo')
            # 移动滑块
            self.move_to_gap(trace)
            sleep(1)
            # browser.get("https://www.tianyancha.com/company/3249343308")
            # time.sleep(2)
            # # 判断是否是验证码页面
            # try:
            #     if "".join(browser.find_element_by_xpath('//div[@class="box2"]//img[@id="targetImgie"]').get_attribute('src')):
            #         print("出现验证码")
            #         # wait = WebDriverWait(browser,10)
            #         # 右键单击图片
            #         a_img = wait.until(EC.element_to_be_clickable((By.ID,"targetImgie")))
            #         # 执行鼠标动作
            #         actions = ActionChains(browser)
            #         # 找到图片后右键单击图片
            #         actions.context_click(a_img)
            #         actions.perform()
            #         # 发送键盘按键，根据不同的网页，
            #         # 右键之后按对应次数向下键，
            #         # 找到图片另存为菜单
            #         pyautogui.typewrite(['down','down','enter'])
            #         # 单击图片另存之后等1s敲回车
            #         sleep(1)
            #         pyautogui.typewrite(['enter'])
            #         time.sleep(2)
            #         b_img = wait.until(EC.element_to_be_clickable((By.ID,"bgImgie")))
            #         # 执行鼠标动作
            #         actions = ActionChains(browser)
            #         # 找到图片后右键单击图片
            #         actions.context_click(b_img)
            #         actions.perform()
            #         # 发送键盘按键，根据不同的网页，
            #         # 右键之后按对应次数向下键，
            #         # 找到图片另存为菜单
            #         pyautogui.typewrite(['down','down','enter'])
            #         # 单击图片另存之后等1s敲回车
            #         sleep(1)
            #         pyautogui.typewrite(['enter'])
            #         time.sleep(3)
            #         # 下载好两张验证码后引入拼接程序
            #         from pinjie import pinjie
            #         pinjie("C:\\Users\Administrator\Downloads\下载.png", "C:\\Users\Administrator\Downloads\下载 (1).png")
            #         sleep(15) # 拼接需要一个过程，有点耗时
            #         # 删除掉png格式图片（上面下载好的两张验证码）为了下一个ID存储验证码提供便利
            #         path = "C:\\Users\Administrator\Downloads\\"
            #         filenames = os.listdir("C:\\Users\Administrator\Downloads\\")
            #         for filename in filenames:
            #             if ".png" in filename:
            #                 os.remove(path+filename)
            #         # 定位验证码坐标
            #         imgelement = browser.find_element_by_xpath('//div[@class="box2"]//img[@id="targetImgie"]')
            #         location = imgelement.location
            #         print(location)
            #         # 接入超级鹰打码平台
            #         chaojiying = Chaojiying_Client("L54555", "Li891004", '90004')
            #         im = open('images/out.png', 'rb').read()
            #         # 获取超级鹰返回坐标
            #         r_json = chaojiying.PostPic(im, 9004)
            #         print(r_json)
            #         if r_json:
            #             pic_str = r_json["pic_str"].split('|')
            #
            #             for pic in pic_str[:]:
            #                 pic_x = pic.split(',')[0]
            #
            #                 pic_y = pic.split(',')[1]
            #                 self.click_locxy(browser, location['x']-652+int(pic_x), location['y']-330+int(pic_y), left_click=True) # 左键点击
            #         time.sleep(1)
            #         browser.find_element_by_xpath('//div[@class="container"]/div/div/div[3]/div[2]').click()
            #         time.sleep(2)
            #         # 获取cookie值
            #         try:
            #             # 用取值的方法检查是否验证成功
            #             if "".join(browser.find_element_by_xpath('//div[@class="box -company-box "]/div[@class="content"]/div[@class="header"]/h1[@class="name"]').text):
            #                 cookie_items = browser.get_cookies()
            #                 cookies = ""
            #
            #                 for cookie in cookie_items:
            #                     cookies += cookie['name']+'='+cookie['value']+';'
            #                 time.sleep(3)
            #                 browser.close()
            #                 return cookies
            #         except Exception as e:
            #             cookies = ""
            #             browser.close()
            #             return cookies
            # except Exception as e:
            #     path = "C:\\Users\Administrator\Downloads\\"
            #     filenames = os.listdir("C:\\Users\Administrator\Downloads\\")
            #     for filename in filenames:
            #         if ".png" in filename:
            #             os.remove(path+filename)
            #     # 获取cookie值
            #     try:
            #         # 用取值的方法检查是否登陆成功
            #         if "".join(browser.find_element_by_xpath('//div[@class="box -company-box "]/div[@class="content"]/div[@class="header"]/h1[@class="name"]').text):
            #             cookie_items = browser.get_cookies()
            #             cookies = ""
            #             for cookie in cookie_items:
            #                 cookies += cookie['name']+'='+cookie['value']+';'
            #             time.sleep(3)
            #             browser.close()
            #             return cookies
            #     except Exception as e:
            #         cookies = ""
            #         browser.close()
            #         return cookies


            # cookie_items = browser.get_cookies()
            # cookies = ""
            # for cookie in cookie_items:
            #     cookies += cookie['name']+'='+cookie['value']+';'
            # time.sleep(2)
            # browser.close()
            # return cookies

            time.sleep(1)
            cookies = {}
            cookie_list = browser.get_cookies()
            for i in cookie_list:
                key = i.get('name')
                value = i.get('value')
                cookies[key] = value
            send = Send_Click(url='https://www.tianyancha.com/usercenter/myorder', cookies=cookies)
            result = send.run()
            if result == 200:
                cookie_items = browser.get_cookies()
                cookies = ""
                for cookie in cookie_items:
                    cookies += cookie['name']+'='+cookie['value']+';'

                browser.close()
                return cookies
            else:
                browser.close()
                return ''
        except:
            browser.close()


class Getter:
    def __init__(self, website='tianyancha'):
        """初始化数据库类和cookie爬虫类"""
        self.website = website
        self.redis = RedisClient('accounts', self.website)
        self.crawler = Crawler()
        self.accounts_db = RedisClient('accounts', self.website)

    def is_over_threshold(self):
        """判断数据库是否已经存满"""
        if self.redis.count() >= POOL_UPPER_THRESHLD:
            return True
        return False

    def run(self):
        """开始抓取cookies存入数据库"""
        accounts_usernames = self.accounts_db.usernames()
        keys = self.redis.get()
        for username in accounts_usernames[:]:
            if not username in keys:
                password = self.accounts_db.get_value(username)
                logger.info(f'正在生成Cookies - 账号 {username} - 密码 {password}')
                if not self.is_over_threshold():
                    try:
                        time.sleep(5)
                        cookie = self.crawler.crawl_main(username, password)
                        if cookie:
                            self.redis.add(username, cookie)
                            logger.info(f"账号 {username} cookie有效")
                        else:
                            logger.info("监控到cookie为空, 登录失败")
                    except Exception as e:
                        logger.warning(f'请求出错 - {e}')
            else:
                # print('账号', username, "存在于cookie池里")
                pass


if __name__ == '__main__':
    a = Getter()
    a.run()
