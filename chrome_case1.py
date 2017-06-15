import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = '/Users/Shadow/Downloads/Imperial/Individual/selenium/chromedriver'
a = '--load-extension='
extension_p = '/Users/Shadow/Downloads/Imperial/Individual/selenium/ecap.crx'
extension_list = 'chrome://extensions-frame'
extension_option = 'chrome-extension://bjloopkdhkfpllfogfeboofijlenbbie/options.html'
url = 'http://www.baidu.com'
ID = 'bjloopkdhkfpllfogfeboofijlenbbie'
download = './'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download}

cmd = 'chrome-extension://' + ID + '/command.html?'
start = 'start'
stop = 'stop'
toggle = 'toggle'
save = 'save'
clear = 'clear'

doc = '/Users/Shadow/Downloads/'
test = 'ECAP_G_2017-06-14T12-39-51.155Z.json'


def send_cmd(br, command):
    br.get(command)


# Different test case have different interaction to simulate real user
def interaction(br, type):
    br.implicite_wait(5)


def analyse_json(path):
    fd = open(doc + test, 'r')
    data = json.load(fd)

    for package in data:
        if package['type'].count('tab') > 0 or package['type'].count('navigation') > 0 \
                or package['type'].count('window') > 0:
            continue

    print data




# browser.get(extension_option)
# browser.find_element_by_id('autoStart').click()


# browser.get(cmd + start)

# search = browser.find_element_by_id("kw")
# search.send_keys('test')
# click = browser.find_element_by_id("su")
# click.send_keys(Keys.RETURN)
# browser.get(extension_list)

if __name__ == '__main__':

    listener = Options()
    listener.add_extension(extension_p)
    listener.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(path, chrome_options=listener)

    # send_cmd(browser, cmd + start)

    case = sys.argv[1]

    analyse_json(path + test)

    # Need modified
    fd = open('shoes_case1.txt')
    for i in fd:
        send_cmd(browser, cmd + clear)
        browser.get(i)
        send_cmd(browser, cmd + save)
        analyse_json(download)

    # print browser.title
    # print browser.page_source


#browser.quit()