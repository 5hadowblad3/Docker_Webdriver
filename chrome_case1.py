import os
import sys
import json
import time
import shutil
import urlparse
import tldextract
import editdistance
from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

driver_path_mac = './chromedriver_mac'
driver_path_linux = './chromedriver_linux'
extension_name = 'listener'
extension_path = 'src.crx'
extension_list = 'chrome://extensions-frame'
extensions = 'chrome-extension://'
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
cookies_set = {}


def load_data(path):
    datas = open(path, 'r')
    features = []
    targets = []

    for data in datas:
        if len(data) == 1:
            continue

        target = int(data[-2])
        feature = []
        for element in data[:-3]:
            if element != ' ':
                feature.append(int(element))

        features.append(feature)
        targets.append(target)

    return targets, features


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def configuration(br, ID):
    br.get(extensions + ID + '/options.html')
    br.find_element_by_id('autoStart').click()
    br.find_element_by_id('interactive').click()
    br.find_element_by_id('autoSaveEvery').send_keys('10000')
    br.find_element_by_id('save').send_keys(Keys.RETURN)


def get_ID(br, e_name):
    br.get('chrome://extensions-frame')
    names = br.find_elements_by_xpath("//div[@id='extension-settings-list']/div/div/div/div/h2")
    ID = br.find_elements_by_class_name('extension-list-item-wrapper')

    for ind, name in enumerate(names):
        # print str(name.text), isinstance(str(name.text), str), len(str(name.text))
        if cmp(str(name.text), e_name) == 0:
            return str(ID[ind].get_attribute('id'))


def send_cmd(br, command):
    br.get(command)


# Different test case have different interaction to simulate real user
def interaction(br, type):
    br.implicitly_wait(5)


# label preparation
def init_label():
    flag = {
        'variable_new': 0,
        'variable_change': 0,
        'cookies_change': 0,
        'dom': 0,
        'request_length': 0,
        'response_length': 0,
        'cookies_number': 0,
        'parameter_number': 0,
        'js_number': 0,
        'request_number': 0,
        'ip_cnt': 0,
        'new_window': 0,
        'new_frame': 0,
        'frame_changed': 0,


        # header info
        'user-agent': 0,
        'cookies': 0,
        'Referer': 0,
        'Accept-Encoding': 0,
        'Accept-Language': 0,
        'ETag': 0,
        'last-modified': 0,
        'set-cookie': 0,
        'cache-control': 0,

        # cookies feature
        'multi-origin': 0,
        'engine-result': 0,

        # final label
        'label': 0
    }

    return flag

# JS feature analysis
def analysis_js(content, label):
    # wait for finish
    return label


# Cookie feature analysis
def analysis_cookie(cookies, domain, label):
    for cookie in cookies.keys():
        # pass
        for ck in cookies_set[cookies]:
            if ck['value'] == cookies[cookie]:
                if label['multi-origin'] != 1 and domain != ck['origin']:
                    label['multi-origin'] = 1
                    break


# Json file analysis
def analyse_json(path, location):
    fd = open(path, 'r')
    fd2 = open(location, 'a')
    data = json.load(fd)
    label = init_label()
    request_cnt = 0
    js_cnt = 0
    ip = []
    urls = []
    cookies = {}

    # analysis each behavior inside one website
    for package in data:
        # situation ignored
        if package['type'].count('tab') > 0 or package['type'].count('navigation') > 0 \
                or package['type'].count('window') > 0:
            continue

        # interaction with third party => tracking
        if package['type'] == 'request':
            url = tldextract.extract(package['details']['url'])
            if (url.domain + '.' + url.suffix) not in urls:
                urls.append(url.domain + '.' + url.suffix)
                label['label'] = 1
            else:
                pass

            if package['details']['url'].count('.js') > 0:
                js_cnt += 1

            request_cnt += 1

        # new windows generated
        if package['type'] == 'request' or package['type'] == 'response':
            if package['details']['parentFrameId'] != -1:
                label['new_window'] = 1

        # parameter number
        if package['details']['url'].count('=') > 0:
            label['parameter_number'] = 1

        # upload (hidden) text 1
        if label['variable_new'] != 1 and package['type'] == 'variable.new' > 0:
            label['variable_new'] = 1

        # local storage modification 1
        if label['variable_change'] != 1 and package['type'] == 'variable.change':
            label['variable_change'] = 1

        # request headers analysis 8
        if package['type'].count('request') > 0:
            length = 0
            request_cnt += 1
            # print package['details']['type']
            if package['details']['type'] != 'main_frame' or package['details']['url'].count('chrome-extension') > 0:
                continue
            else:
                domain = urlparse.urlparse(package['details']['url']).netloc
                # print 'enter ', domain
                if 'requestHeaders' in package['details']:
                    for header in package['details']['requestHeaders']:
                        length += len(header['value'])
                        # user agent exchanging
                        if label['user-agent'] != 1 and header['name'].count('user-agent'):
                            label['user-agent'] = 1

                        # request with cookies
                        if label['cookies'] != 1 and header['name'].count('cookies') > 0:
                            label['cookies'] = 1

                        # check for referer header
                        if label['Referer'] != 1 and header['name'].count('Referer') > 0:
                            if header['value'] != domain:
                                label['label'] = 1
                            label['Referer'] = 1

                        # check for font info
                        if label['Accept-Encoding'] != 1 and header['name'].count('Accept-Encoding') > 0:
                            label['Accept-Encoding'] = 1

                        if label['Accept-Encoding'] != 1 and header['name'].count('Accept-Language') > 0:
                            label['Accept-Encoding'] = 1

                        if label['ETag'] != 1 and header['name'].count('ETag') > 0:
                            label['ETag'] = 1

                # request length
                if length > 120:
                    label['request_length'] = 1

        # response headers analysis
        if package['type'].count('response') > 0:
            length = 0
            if 'ip' in package['details'] and package['details']['ip'] not in ip:
                ip.append(package['details']['ip'])

            if package['details']['type'] != 'main_frame' or package['details']['url'].count('chrome-extension') > 0:
                continue
            else:
                # print package['details']['type']
                # print 'response from ', domain
                for header in package['details']['responseHeaders']:
                    length += len(header['value'])
                    # user agent exchanging
                    if label['last-modified'] != 1 and header['name'].count('last-modified'):
                        label['last-modified'] = 1

                    # response with cookies
                    if header['name'].count('set-cookie') > 0:
                        label['set-cookie'] = 1
                        if len(cookies.keys()) > 0:
                            target_cookies = str(header['value']).split('; ')
                            for target_cookie in target_cookies:
                                name = target_cookie.split('=')[0]
                                value = target_cookie.split('=')[1]
                                cookies[name] = value
                                if name not in cookies_set.keys():
                                    cookies_set[name] = []
                                    tmp = {'value': value}
                                    cookies_set[name]['value'] = value
                                    url = tldextract.extract(package['details']['url'])
                                    tmp['origin'] = url.domain + '.' + url.suffix
                                    cookies_set[name].append(tmp)
                                else:
                                    if value in cookies_set[name]:
                                        flag = 1
                                    else:
                                        cookies_set[name].append(value)

                    # cache control type
                    if label['cache-control'] != 1 and header['name'].count('cache-control') > 0:
                        label['cache-control'] = 1

                # response length
                if length > 120:
                    label['response_length'] = 1

        # cookies modification 1
        if label['cookies_change'] != 1 and package['type'] == 'cookie.changed':
            label['cookies_change'] = 1

        # dom element changing 1
        if label['dom'] != 1 and package['type'].count('dom') > 0:
            label['dom'] = 1

    # js number
    if js_cnt > 10:
        label['js_number'] = 1

    # ip number
    if len(ip) > 4:
        label['ip_cnt'] = 1

    # request number
    if request_cnt > 20:
        label['request_number'] = 1

    if len(cookies.keys()) > 5:
        label['cookies_number'] = 1

    # cookies pattern increase
    # label = analysis_cookie(cookies, domain, label)

    for key, value in label.iteritems():
        fd2.write(str(value) + ' ')

    # save final mark
    fd2.write(str(label['label']) + '\n')


# machine learning analysis
def ml_performance(path):
    target, features = load_data(path)
    clf = RandomForestClassifier(n_estimators=10)
    # clf = clf.fit(features, target)
    clf2 = DecisionTreeClassifier(max_depth=None, min_samples_split=2, random_state=0)
    clf3 = AdaBoostClassifier(n_estimators=100)
    clf4 = MLPClassifier()
    cl5 = svm.SVC()
    scores = cross_val_score(clf, features, target)
    scores2 = cross_val_score(clf2, features, target)
    scores3 = cross_val_score(clf3, features, target)
    scores4 = cross_val_score(clf4, features, target)
    # scores5 = cross_val_score(cl5, features, target)
    # scores4 = cross_val_score(clf4, features, target)

    print scores.mean()
    print scores2.mean()
    print scores3.mean()
    print scores4.mean()
    # print scores5.mean()


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

    # browser = webdriver.Chrome(chrome_options=listener)
    browser = webdriver.Chrome(driver_path_mac, chrome_options=listener)

    extension_id = get_ID(browser, extension_name)
    cmd = 'chrome-extension://' + extension_id + '/command.html?'

    # search = browser.find_element_by_id("kw")
    # search.send_keys('test')

    # send_cmd(browser, cmd + start)

    # case = sys.argv[1]

    # analyse_json(path + test)

    # Need modified
    fd = open('food_case2.txt')
    # configuration(browser, extension_id)

    send_cmd(browser, cmd + start)

    # main_handle = browser.current_window_handle
    # ActionChains(browser).key_down(Keys.COMMAND).send_keys("t").key_up(Keys.COMMAND).perform()

    # for handle in browser.window_handles:
    #     if handle != main_handle:
    #         extension_handle = handle
    #         break

    for i in fd:
        print i
        if len(i) < 3:
            continue
        # send_cmd(browser, cmd + clear)

        try:
            browser.get(i)
        except TimeoutException:
            print 'no reaction, pass this site'
            continue

        try:
            WebDriverWait(browser, 1).until(EC.alert_is_present())
            alert = browser.switch_to.alert()
            alert.accept()
        except TimeoutException:
            print 'no alert'

        interaction(browser, 1)
        # print cmd + save
        send_cmd(browser, cmd + save)
        time.sleep(2)
        files = os.listdir(download_path)
        # print files

        if len(files) == 0:
            print 'error in saving'
            break

        for file in files:
            name, ext = os.path.splitext(file)
            # print ext
            if ext == '.json':
                json_file = name + ext
                # print json_file
                break

        # json_file = os.listdir(download_path)[0]
        # print  download_path + json_file
        analyse_json(download_path + json_file, 'data_set')
        shutil.move(download_path + json_file, backup_path + json_file)


    # print browser.title
    # print browser.page_source
    ml_performance('data_set')
    # browser.quit()
