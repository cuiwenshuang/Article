# -*- coding: utf-8 -*- 
# @Time : 2019/12/2 0002 17:28 
# @Author : cuiws 
# @File : Republish.py
#发布文章
phone='15527959558'


from selenium import webdriver
from selenium.webdriver import ChromeOptions
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])#
login_url="https://sso.toutiao.com/login/?service=https://mp.toutiao.com/sso_confirm/?redirect_url=L3Byb2ZpbGVfdjMvZ3JhcGhpYy9wdWJsaXNo"
url = "https://mp.toutiao.com/profile_v3/graphic/publish"
driver = webdriver.Chrome("util/chromedriver.exe",chrome_options=option)
driver.get(login_url)
driver.find_element_by_class_name("bytedance-input").send_keys(phone)
driver.implicitly_wait(5)
driver.find_element_by_class_name("mobile-code-get").click()
print("等待填写验证码")
driver.implicitly_wait(20)
driver.find_elements_by_id("bytedance-login-submit").click()#登陆




# import webbrowser
# webbrowser.open("")


# from splinter import Browser
#
# browser = Browser(driver_name='chrome')
# browser.visit(login_url)






