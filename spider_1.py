#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/16 8:56
# @Author  : Py.qi
# @File    : spider_1.py
# @Software: PyCharm

import time
from PIL import Image
from io import BytesIO
from selenium import webdriver
from day33_yangzheng.chaojiying import Chaojiying_Client
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq

#网站登陆用户名、密码
url='https://kyfw.12306.cn/otn/login/init'
USERNAME='zxq920664709'
PASSWORD='zxq1985129'
#超级鹰用户名、密码、软件ID、验证码类型
CHAOJIYING_USERNAME='zxq920664709'
CHAOJIYING_PASSWORD='zxq1985129'
CHAOJIYING_SOFT_ID=896859
CHAOJIYING_KIND=9004
#查询信息
chufadi='北京'
mudedi='上海'
chufari='2018-07-17'
chufaris=['2018-07-16','2018-07-17','2018-07-18','2018-07-19','2018-07-20']
#G高铁，D动车，Z直达，T特快，K快速
checi=['G','D','Z','T','K']

class spider_chepiao(object):
    '''
    初始化spider_chepiao
    '''
    def __init__(self):
        self.url=url
        self.driver=webdriver.Chrome()
        self.wait=WebDriverWait(self.driver,20)
        self.username=USERNAME
        self.password=PASSWORD
        self.chaojiying=Chaojiying_Client(CHAOJIYING_USERNAME,CHAOJIYING_PASSWORD,CHAOJIYING_SOFT_ID)


    def send_to_userandpass(self):
        '''
        发送用户名及密码
        :return: None
        '''
        login_user=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#username')))
        login_passwd=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#password')))
        login_user.send_keys(self.username)
        login_passwd.send_keys(self.password)

    def get_touclick_element(self):
        '''
        获取验证图片对象
        :return: 返回图片对象
        '''
        image_obj = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.touclick-wrapper')))
        return image_obj

    def get_touclck(self,img):
        '''
        截取图片
        :param img: 保存图像地址
        :return: 图像数据
        '''
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.touclick-image')))
        image_source=self.driver.get_screenshot_as_png()
        image_obj=self.get_touclick_element()
        location = image_obj.location
        size = image_obj.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        print(left,top,right,bottom)
        image=Image.open(BytesIO(image_source))
        crop_image=image.crop((left,top,right,bottom))
        crop_image.save(img)
        return crop_image

    def get_points(self,result):
            '''
            解析识别坐标
            :param result:识别结果
            :return: 转化后的结果
            '''
            groups = result.get('pic_str').split('|')
            locations = [[int(number) for number in group.split(',')] for group in groups]
            return locations

    def touch_click_words(self,locations):
        '''
        点击验证图片
        :param locations: 点击位置坐标
        :return: None
        '''
        for location in locations:
            print(location)
            ActionChains(self.driver).move_to_element_with_offset(self.get_touclick_element(),location[0],location[1]).click().perform()

    def login(self):
        '''
        点击登陆
        :return:None
        '''
        login_element=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginSub')))
        login_element.click()
        time.sleep(2)
        print('登陆成功！')

    def main(self):
        '''
        主调用函数
        :return:
        '''
        self.driver.get(self.url)
        #输入用户名与密码
        self.send_to_userandpass()
        while self.driver.current_url != 'https://kyfw.12306.cn/otn/index/initMy12306':
            #获取验证吗图片
            image=self.get_touclck('cropimage.png')
            bytes_array=BytesIO()
            bytes_array.getvalue()
            image.save(bytes_array,format('PNG'))
            #识别验证码
            result=self.chaojiying.PostPic(bytes_array.getvalue(),CHAOJIYING_KIND)
            #解析验证码
            locations=self.get_points(result)
            #点击验证
            self.touch_click_words(locations)
            time.sleep(3)
            click_image=self.driver.get_screenshot_as_png()
            img=BytesIO(click_image)
            Image.open(img).save('click_image.png')
            #点击登陆
            self.login()
            time.sleep(4)
    def yudingchepiao(self):
        try:
            #转到车票预订页面
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#selectYuding'))).click()
            time.sleep(2)
            #出发车站
            fromstationText=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#fromStationText')))
            #目的车站
            toStationText=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#toStationText')))
            #出发日期
            train_date=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#train_date')))
            #高铁
            G_gaotie=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#checkbox_aJw68Auir6')))
            #动车
            D_dongche=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#checkbox_lLbTP5dXQV')))
            #直达
            Z_zhida=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#checkbox_uV849wkRQE')))
            #特快
            T_tekuai=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#checkbox_8U5E58vOFt')))
            #快速
            K_kuaisu=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#checkbox_ROZEXsgP1x')))
            #查询按钮
            chaxun=self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#query_ticket')))

            fromstationText.send_keys(chufadi)
            toStationText.send_keys(mudedi)
            train_date.send_keys(chufari)
            if 'G' in checi:
                G_gaotie.click()
            elif 'D' in checi:
                D_dongche.click()
            elif 'Z' in checi:
                Z_zhida.click()
            elif 'T' in checi:
                T_tekuai.click()
            elif 'K' in checi:
                K_kuaisu.click()
            chaxun.click()
        except TimeoutException as e:
            print('connect on timeout')
        finally:
            html = self.driver.page_source
            return html

    def parse_html(self,html):
        '''
        解析源码返回数据
        :param html: html源码
        :return:
        '''
        doc=pq(html,parser='html')
        items=doc('#queryLeftTable .bgc').items()
        for i in items:
            print(i.text())


if __name__ == '__main__':
    tielu=spider_chepiao()
    tielu.main()
    html=tielu.yudingchepiao()
    tielu.parse_html(html)