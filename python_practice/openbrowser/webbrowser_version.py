# read offical doc from https://docs.python.org/3.7/library/webbrowser.html?highlight=webbrowser#webbrowser.get

import webbrowser
#print(webbrowser._browsers)
chrome_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
firefox_path=r'C:\Program Files\Mozilla Firefox\firefox.exe'
url = 'https://@10.57.148.34'


#webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(path))
webbrowser.register('chrome', None, webbrowser.GenericBrowser(chrome_path))
webbrowser.get('chrome').open_new(url)
