from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from pyquery import PyQuery as pq
from urllib.parse import quote
import time
from lxml import etree
import requests

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "localhost:9222") #此处端口保持和命令行启动的端口一致
driver = Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)


# 模拟淘宝登录
def login_taobao():
    print('开始登录...')
    try:
        login_url='https://login.taobao.com/member/login.jhtml'
        driver.get(login_url)
        input_login_id = wait.until(EC.presence_of_element_located((By.ID, 'fm-login-id')))
        input_login_password = wait.until(EC.presence_of_element_located((By.ID, 'fm-login-password')))
        input_login_id.send_keys('') # 用你自己的淘宝账号替换
        input_login_password.send_keys('') # 用你自己的密码替换
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fm-button.fm-submit.password-login')))
        submit.click()
        is_loging = wait.until(EC.url_changes(login_url))
        return is_loging
    except TimeoutException:
        print('login_taobao TimeoutException')
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fm-button.fm-submit')))
        submit.click()
        is_loging = wait.until(EC.url_changes(login_url))
        if is_loging:
            return is_loging
        else:
            login_taobao()


def get_item():
    url = 'https://detail.tmall.com/item.htm?id=770167366835'
    driver.get(url)
    time.sleep(2)
    html = driver.page_source
    doc = pq(html)
    items = doc('.ItemDetail--attrs--3t-mTb3').items()
    for item in items:
        product = {'product': item.find('.Attrs--attr--33ShB6X').text()}
        print(product)

def get_comment():
    url = 'https://detail.tmall.com/item.htm?id=770167366835'
    driver.get(url)
    time.sleep(7)
    comment_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/div[1]/div/div/div[2]/span')))
    comment_btn.click()
    time.sleep(5)
    html = driver.page_source
    doc = pq(html)
    items = doc('.Comments--comments--1662-Lt').items()
    for item in items:
        comment = {'Comment': item.find('.Comment--content--15w7fKj').text()}
        print(comment)


if __name__ == '__main__':
    is_loging=True
    if is_loging:
        print('已经登录')
        time.sleep(3)
        get_item()
        get_comment()
