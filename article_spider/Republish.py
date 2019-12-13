# -*- coding: utf-8 -*- 
# @Time : 2019/12/2 0002 17:28 
# @Author : cuiws 
# @File : Republish.py
#发布文章
#目前因为头条的缓存机制 导致多图模式的文章无法上传 只能发表无封面文章
#问题:
#   1.导入文件方式在多图模式选择图片的时候提示未插入图片 这时需要手动插一张图才能选择文件中的图片做封面
#   2.1的问题可以通过插白图解决 但是下次倒文件进来封面会被上次的封面占住 目前没有去掉的方法
phone='15527959558'

import cv2 as cv
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
import urllib.request
import random
import os
import toutiao_util
from datetime import datetime as dt

#  传入滑块背景图片本地路径和滑块本地路径，返回滑块到缺口的距离
def findPic(img_bg_path, img_slider_path):
    """
    找出图像中最佳匹配位置
    :param img_bg_path: 滑块背景图本地路径
    :param img_slider_path: 滑块图片本地路径
    :return: 返回最差匹配、最佳匹配对应的x坐标
    """

    # 读取滑块背景图片，参数是图片路径，OpenCV默认使用BGR模式
    # cv.imread()是 image read的简写
    # img_bg 是一个numpy库ndarray数组对象
    img_bg = cv.imread(img_bg_path)

    # 对滑块背景图片进行处理，由BGR模式转为gray模式（即灰度模式，也就是黑白图片）
    # 为什么要处理？ BGR模式（彩色图片）的数据比黑白图片的数据大，处理后可以加快算法的计算
    # BGR模式：常见的是RGB模式
    # R代表红，red; G代表绿，green;  B代表蓝，blue。
    # RGB模式就是，色彩数据模式，R在高位，G在中间，B在低位。BGR正好相反。
    # 如红色：RGB模式是(255,0,0)，BGR模式是(0,0,255)
    img_bg_gray = cv.cvtColor(img_bg, cv.COLOR_BGR2GRAY)

    # 读取滑块，参数1是图片路径，参数2是使用灰度模式
    img_slider_gray = cv.imread(img_slider_path, 0)

    # 在滑块背景图中匹配滑块。参数cv.TM_CCOEFF_NORMED是opencv中的一种算法
    res = cv.matchTemplate(img_bg_gray, img_slider_gray, cv.TM_CCOEFF_NORMED)

    print('#' * 50)
    print(type(res))  # 打印：<class 'numpy.ndarray'>
    print(res)
    # 打印：一个二维的ndarray数组
    # [[0.05604218  0.05557462  0.06844381... - 0.1784117 - 0.1811338 - 0.18415523]
    #  [0.06151756  0.04408009  0.07010461... - 0.18493137 - 0.18440475 - 0.1843424]
    # [0.0643926    0.06221284  0.0719175... - 0.18742703 - 0.18535161 - 0.1823346]
    # ...
    # [-0.07755355 - 0.08177952 - 0.08642308... - 0.16476074 - 0.16210903 - 0.15467581]
    # [-0.06975575 - 0.07566144 - 0.07783117... - 0.1412715 - 0.15145643 - 0.14800543]
    # [-0.08476129 - 0.08415948 - 0.0949327... - 0.1371379 - 0.14271489 - 0.14166716]]

    print('#' * 50)

    # cv2.minMaxLoc() 从ndarray数组中找到最小值、最大值及他们的坐标
    value = cv.minMaxLoc(res)
    # 得到的value，如：(-0.1653602570295334, 0.6102921366691589, (144, 1), (141, 56))

    print(value, "#" * 30)

    # 获取x坐标，如上面的144、141
    return value[2:][0][0], value[2:][1][0]


# 返回两个数组：一个用于加速拖动滑块，一个用于减速拖动滑块
def generate_tracks(distance):
    # 给距离加上20，这20像素用在滑块滑过缺口后，减速折返回到缺口
    distance += 20
    v = 0
    t = 0.2
    forward_tracks = []
    current = 0
    mid = distance * 3 / 5  # 减速阀值
    while current < distance:
        if current < mid:
            a = 2  # 加速度为+2
        else:
            a = -3  # 加速度-3
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        current += s
        forward_tracks.append(round(s))

    back_tracks = [-3, -3, -2, -2, -2, -2, -2, -1, -1, -1, -1]
    return forward_tracks, back_tracks

def ParseCookiestr(cookie_str):
    cookie = {}
    for item in cookie_str.split(';'):
        itemname=item.split('=')[0]
        iremvalue=item.split('=')[1]
        name=itemname
        value=urllib.parse.unquote(iremvalue)
        cookie[name]=value
    return cookie



def main():
    img_count = 5
    # 创建一个参数对象，用来控制谷歌浏览器以无界面模式打开
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome('util/chromedriver.exe',chrome_options=chrome_options)

    # 设置浏览器宽高
    # driver.set_window_size(width=2000, height=3000)

    wait = WebDriverWait(driver, 10)

    # cookie_str = 'UM_distinctid=16c0402604a1f0-0f820b01034022-c343162-1fa400-16c0402604b5d1; odin_tt=3b76c8e9bbddd34e275c4dfa2c4677e82d43ccff12fc57a0105be98b189e6196ff1d9d2d11d103d5a0e3799c56244729cad2e78d12b3dfd67a8f3f467d2df1f8; __tea_sdk__ssid=undefined; _ga=GA1.2.256203656.1563446758; _ba=BA0.2-20190724-5110e-5XvtV2mAPI1KM9RHd0Pm; uuid="w:3cf5ef6953a54c1abfae368f8ee32ea4"; tt_webid=6763888485834900999; msh=OFxHiBvU3TYrG8D9XiPfUyZ6cMg; sso_auth_status=b76f932bdde34d4c206005f63c03d5ad; sso_uid_tt=9641895778724bd97248234c41e0f7a5; toutiao_sso_user=7325fd001883c3110fc8b184bff3650b; passport_auth_status=65f02226f9b8d5f623937a610abba11f%2C91d1135ffcb79aed6ae131de5c429ad1; sid_guard=46d80c45af5886f52dd035beaa3ac593%7C1574844799%7C5184000%7CSun%2C+26-Jan-2020+08%3A53%3A19+GMT; sid_tt=46d80c45af5886f52dd035beaa3ac593; sessionid=46d80c45af5886f52dd035beaa3ac593; uid_tt=713d51c736c00511d4379b8585de4f42f42f791a523e85068d085a4b93814e58; SLARDAR_WEB_ID=0f8b0b22-a6e0-467f-8db3-77a5ef45f3f8; _mp_auth_key=b76f932bdde34d4c206005f63c03d5ad; _mp_auth_key=b76f932bdde34d4c206005f63c03d5ad'
    # cookie = ParseCookiestr(cookie_str)
    # driver.add_cookie(cookie)

    driver.get("https://sso.toutiao.com/")


    try:
        # 获取手机号码输入框
        text_box = wait.until(expected_conditions.presence_of_element_located((By.ID, "user-mobile")))
        print(text_box)

        # 获取发送验证按钮
        send_btn = wait.until(expected_conditions.presence_of_element_located((By.ID, "mobile-code-get")))
        print(send_btn)

    except Exception as e:
        print(e)
        raise RuntimeError("获取 手机号码输入框 或者 发送验证按钮 失败，程序结束")

    text_box.send_keys(phone)

    # time.sleep(random.uniform(2, 3))

    try:
        action = ActionChains(driver)
        action.click(send_btn).perform()
    except Exception as e:
        print(e)
    else:
        time.sleep(1.5)

        # 获取 滑块背景图
        bg_image = wait.until(
            expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="captcha_container"]/div/div[2]/img[1]')))

        # bg_image = wait.until(
        #     expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-main"]/img[1]')))
        print("\n背景：")

        print(bg_image)
        bg_image_url = bg_image.get_attribute('src')

        print(bg_image_url)

        # 使用urllib下载背景图
        # 原因是：使用bg_image.screenshot()程序卡在这里，也不报错
        urllib.request.urlretrieve(bg_image_url, "./img_bg.png")

        # 获取 滑块
        slider = wait.until(
            expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="captcha_container"]/div/div[2]/img[2]')))
        # slider = wait.until(
        #     expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-main"]/img[2]')))

        print("\n滑块：")
        print(slider)

        # 注意：千万不能通过截图获取滑块，因为滑块不是规则的图形
        # 而截图截出的是矩形，会把滑块周围的滑块背景图一起截取，势必影响匹配
        # slider.screenshot('./img_slider.png')
        slider_url = slider.get_attribute('src')

        urllib.request.urlretrieve(slider_url, "./img_slider.png")

        value_1, value_2 = findPic('./img_bg.png', './img_slider.png')

        print("#" * 30)
        print("最差匹配和最佳匹配对应的x坐标分别是：")
        print(value_1)
        print(value_2)
        print("#" * 30)

        time.sleep(3)
        forward_tracks, back_tracks = generate_tracks(value_2)
        # 获取滑动按钮
        button = wait.until(
            expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="captcha_container"]/div/div[3]/div[2]/div')))
        # button = wait.until(
        #     expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="validate-drag-button"]/img')))

        action = ActionChains(driver)
        try:
            action.click_and_hold(button).perform()
        except StaleElementReferenceException as e:
            print(e)

        # action.reset_actions()
        time.sleep(3)


        for x in forward_tracks:
            action.move_by_offset(x, 0)  # 前进移动滑块
            print(x)

        print('#' * 50)

        for x in back_tracks:
            action.move_by_offset(x, 0)  # 后退移动滑块
            print(x)


        action.release().perform()

        time.sleep(30)



        #导入文件
        file_list = load_file()
        for file in file_list:
            # 验证码和滑条过后 进入发文章界面
            public_url = "https://mp.toutiao.com/profile_v3/graphic/publish"
            driver.get(public_url)
            time.sleep(5)

            print("导入文件")
            imp_button =  wait.until(expected_conditions.presence_of_element_located((By.XPATH,'//div[@class="syl-toolbar-tool doc_import"]/button/span')))
            print(imp_button)
            imp_button.click()
            time.sleep(5)

            print("导入文件路径")
            sel_button = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//div[@class=' upload-handler']/input")))
            print(sel_button)
            sel_button.send_keys(file)
            time.sleep(5)
            title = str(file).split("/")[-1].replace(".doc","")
            title_area = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//div[@class='editor-title autofit-textarea-wrapper']/textarea")))
            print(title_area)
            title_area.clear()
            title_area.send_keys(title)
            time.sleep(1)
            #设置封面 无图选择无图模式 小于3张选择单图 3张或以上选择三图

            print("拖到底部")

            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            time.sleep(1)

            print("无图模式")
            time.sleep(3)
            check = wait.until(expected_conditions.presence_of_element_located(
                (By.XPATH, "//div[@class='pgc-radio article-cover-radio-group']/label[3]/div/input")))
            time.sleep(2)
            print(check)
            # if img_count==0:
            #     check = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@id='graphic']/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/label[3]/div/input")))
            # elif img_count<3:
            #     check = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@id='graphic']/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/label[1]/div/input")))
            # else:
            #     check = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//*[@id='graphic']/div/div[2]/div/div[2]/div[1]/div/div[2]/div/div[1]/label[2]/div/input")))
            check.click()
            time.sleep(2)

            republic = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//button[@id='publish']")))
            print("发布 %s"%republic)
            republic.click()
            toutiao_util.write_log("file[%s] 发布完成"%file)

            alert = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//div[@class='tui2-modal-body']")))
            if alert!=None:
                # not_check = wait.until(expected_conditions.presence_of_element_located((By.XPATH,"//button[@class='tui2-btn tui2-btn-size-default tui2-btn-default']")))
                check = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//button[@class='tui2-btn tui2-btn-size-default tui2-btn-primary']")))
                check.click()
                time.sleep(2)
                #切换到新标签页
                current_windows = driver.current_window_handle
                all_handles = driver.window_handles
                #关闭原有的标签页
                driver.close()
                for handle in all_handles:
                    if handle != current_windows:  # 判断条件
                        driver.switch_to.window(handle)
                        break
            time.sleep(5)
    finally:
        time.sleep(10000)
        driver.close()


def load_file():
    file_list = []
    upper = os.path.abspath(os.path.join(os.getcwd(), ".."))
    source = os.path.join(upper, 'source').replace("\\", "/")
    date = str(dt.now().date())
    file_path = os.path.join(source,date).replace("\\", "/")

    for root, dirs, files  in os.walk(file_path):
        for file in files:
            if str(file).endswith(".doc"):
                file_path_abs = os.path.join(file_path,file).replace("\\", "/")
                print(file_path_abs)
                title = str(file).split("/")[-1].replace(".doc", "")
                file_list.append(file_path_abs)
    return file_list



if __name__ == '__main__':
    main()
    # load_file()








