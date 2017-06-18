import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = './chromedriver'
a = '--load-extension='
extension_p = 'ecap.crx'
extension_list = 'chrome://extensions-frame'
extension_option = 'chrome-extension://bjloopkdhkfpllfogfeboofijlenbbie/options.html'
url = 'http://www.baidu.com'

download = './'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download}

start = 'start'
stop = 'stop'
toggle = 'toggle'
save = 'save'
clear = 'clear'

doc = '/Users/Shadow/Downloads/'
test = 'ECAP_G_2017-06-14T12-39-51.155Z.json'


def get_ID(br):
    br.get('chrome://extensions-frame')
    names = br.find_elements_by_xpath("//div[@id='extension-settings-list']/div/div/div/div/h2")
    ID = br.find_elements_by_class_name('extension-list-item-wrapper')

    for ind, name in enumerate(names):
        print str(name.text), isinstance(str(name.text), str), len(str(name.text))
        if cmp(str(name.text), 'listener') == 0:
            return str(ID[ind].get_attribute('id'))


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
                or package['type'].count('window') > 0 or package['type'].count('variable') > 0:
            continue

    print data




# browser.get(extension_option)
# browser.find_element_by_id('autoStart').click()


# browser.get(cmd + start)


# click = browser.find_element_by_id("su")
# click.send_keys(Keys.RETURN)
# browser.get(extension_list)

if __name__ == '__main__':

    listener = Options()
    listener.add_extension(extension_p)
    listener.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(path, chrome_options=listener)

    print get_ID(browser)

    cmd = 'chrome-extension://' + get_ID(browser) + '/command.html?'
    cmd = 'chrome-extension://' + get_ID(browser) + '/command.html?'

    # search = browser.find_element_by_id("kw")
    # search.send_keys('test')


    # send_cmd(browser, cmd + start)

    # case = sys.argv[1]

    # analyse_json(path + test)
    # print 'hello world'
    # Need modified
    # fd = open('shoes_case1.txt')
    # for i in fd:
    #     send_cmd(browser, cmd + clear)
    #     browser.get(i)
    #     send_cmd(browser, cmd + save)
    #     analyse_json(download)

    # print browser.title
    # print browser.page_source


#browser.quit()