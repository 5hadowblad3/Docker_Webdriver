import os
import sys
import json
import time
import shutil
import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

driver_path = './chromedriver'
a = '--load-extension='
extension_name = 'listener'
extension_path = 'ecap.crx'
extension_list = 'chrome://extensions-frame'

url = 'http://www.baidu.com'

download_path = './json/'
backup_path = './backup/'
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_path}

start = 'start'
stop = 'stop'
toggle = 'toggle'
save = 'save'
clear = 'clear'

data_set = 'dataset1'


def get_ID(br, e_name):
    br.get('chrome://extensions-frame')
    names = br.find_elements_by_xpath("//div[@id='extension-settings-list']/div/div/div/div/h2")
    ID = br.find_elements_by_class_name('extension-list-item-wrapper')

    for ind, name in enumerate(names):
        print str(name.text), isinstance(str(name.text), str), len(str(name.text))
        if cmp(str(name.text), e_name) == 0:
            return str(ID[ind].get_attribute('id'))


def send_cmd(br, command):
    br.get(command)


# Different test case have different interaction to simulate real user
def interaction(br, type):
    br.implicite_wait(5)


def analyse_json(path, location):
    fd = open(path, 'r')
    fd2 = open(location, 'a')
    data = json.load(fd)
    flag = 0
    url = ''
    instance = []

    for package in data:
        if package['type'].count('tab') > 0 or package['type'].count('navigation') > 0 \
                or package['type'].count('window') > 0:
            continue

        # interaction with third party => tracking
        if package['type'] == 'request':
            if len(url) == 0:
                url = package['details']['url']
            elif url != str(package['details']['url']):
                flag = 1

        # upload (hidden) text
        if package['type'] == 'variable.new' and package['details']['type'].count('input') > 0:
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # local storage modification
        if package['type'] == 'variable.change':
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # user agent exchanging
        if package['type'].count('request') > 0 and package['details']['responseHeaders'].count('user-agent'):
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # request with cookies
        if package['type'].count('request') > 0 and package['details']['responseHeaders'].keys().find('cookies') != -1:
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # cookies given in the response
        if package['type'].count('response') > 0 and \
                        package['details']['responseHeaders'].keys().find('set-cookie') != -1:
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # cookies modification
        if package['type'] == 'cookie.changed':
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # dom element changing
        if package['type'].count('dom') > 0:
            fd2.write('1 ')
            instance.append(1)
        else:
            fd2.write('0 ')
            instance.append(0)

        # save final marke
        fd2.write(str(flag))
        instance.append(flag)

        # save marked instance
        data.append(instance)

        return data

# browser.get(extension_option)
# browser.find_element_by_id('autoStart').click()
# browser.get(cmd + start)


# click = browser.find_element_by_id("su")
# click.send_keys(Keys.RETURN)
# browser.get(extension_list)

if __name__ == '__main__':

    listener = Options()
    listener.add_extension(extension_path)
    listener.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(chrome_options=listener)
   # browser = webdriver.Chrome(driver_path, chrome_options=listener)
    print 'enter'
    print get_ID(browser, extension_name)

    cmd = 'chrome-extension://' + get_ID(browser, extension_name) + '/command.html?'

    # search = browser.find_element_by_id("kw")
    # search.send_keys('test')

    # send_cmd(browser, cmd + start)

    # case = sys.argv[1]

    # analyse_json(path + test)

    print 'hello world'
    # Need modified
    fd = open('food_case22.txt')
    send_cmd(browser, cmd + start)
    for i in fd:
        print i
        if len(i) < 3:
            continue
        print 'filter: ' + i
        send_cmd(browser, cmd + clear)
        browser.get(i)
        send_cmd(browser, cmd + save)
        time.sleep(5)
        files = os.listdir(download_path)
        print files

        if len(files) == 0:
            print 'error in saving'
            break

        for file in files:
            name, ext = os.path.splitext(file)
            print ext
            if ext =='.json':
                json_file = name + ext
                break

        json_file = os.listdir(download_path)[0]
        analyse_json(download_path + json_file, 'data_set')
        shutil.move(download_path + json_file, backup_path + json_file)

    # print browser.title
    # print browser.page_source


    browser.quit()
