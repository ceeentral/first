from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import selenium

chromedriver = r'D:\quicktest\chromedriver_win32\chromedriver.exe'
browser = webdriver.Chrome(chromedriver)
browser.get('https://10.57.148.34')

username = browser.find_element_by_id("applicationLoginUsername")  #could find the applicationLoginUsername through click F12, and search one by one hahahah
password = browser.find_element_by_id("applicationLoginPassword")

username.send_keys("xx")
password.send_keys("aa")

browser.find_element_by_id("applicationLoginButton").click()