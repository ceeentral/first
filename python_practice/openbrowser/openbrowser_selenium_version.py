from selenium import webdriver
from selenium.webdriver.common.keys import Keys

ippool={"gnb":"https://10.57.148.34", "lte":"https://10.57.146.66"}

def openweb(url):
	chromedriver = r'D:\quicktest\chromedriver_win32\chromedriver.exe'
	global browser
	browser = webdriver.Chrome(chromedriver)
	browser.get(url)
def fill_and_click_gnb():
	username = browser.find_element_by_id("applicationLoginUsername")  #could find the applicationLoginUsername through click F12, and search one by one hahahah
	password = browser.find_element_by_id("applicationLoginPassword")
	username.send_keys("aa")
	password.send_keys("xx")
	browser.find_element_by_id("applicationLoginButton").click()
def fill_and_click_lte():
	username = browser.find_element_by_class_name("input-username").find_element_by_name("userName")
	password = browser.find_element_by_class_name("input-password").find_element_by_name("password")
	username.send_keys("aa")
	password.send_keys("xx")
	browser.find_element_by_class_name("login-buttons").find_element_by_class_name("ng-isolate-scope").click()

def main():
	iptype=input("please choose ip to connect:\n \
	0 for 10.57.148.34 \n \
	1 for 10.57.146.66\n")
	if iptype == '0':
		ip = ippool['gnb']
		openweb(ip)
		fill_and_click_gnb()
	elif iptype == '1':
		ip = ippool['lte']
		openweb(ip)
		fill_and_click_lte()
main()
	

