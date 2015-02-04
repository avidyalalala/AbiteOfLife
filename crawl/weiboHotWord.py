
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from random import choice
import re

browser = webdriver.Firefox()
wait = ui.WebDriverWait(browser,10)
browser.get("http://d.weibo.com/102803?feed_sort=102803_ctg1_99991_-_ctg1_99991&feed_filter=102803_ctg1_99991_-_ctg1_99991#Pl_Core_MixedFeed__5")
wait.until(lambda browser: browser.find_element_by_xpath("//a[@node-type='loginBtn']"))
browser.find_element_by_xpath("//a[@node-type='loginBtn']").click()
wait.until(lambda browser: browser.find_element_by_xpath("//input[@name='username']"))
user = browser.find_element_by_xpath("//input[@name='username']")
user.clear()
user.send_keys("linalovebaby@gmail.com")
psw = browser.find_element_by_xpath("//input[@name='password']")
psw.clear()
psw.send_keys("ilovenana")
browser.find_element_by_xpath("//a[@node-type='submitBtn']").click()
wait.until(lambda browser: browser.find_element_by_xpath("//div[@node-type='feed_list_content']"))
contents=browser.find_elements_by_xpath("//div[@node-type='feed_list_content']")
for content in contents:

    print(content.text)
