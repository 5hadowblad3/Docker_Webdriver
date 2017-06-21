from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

path = '/Users/Shadow/Downloads/Imperial/Individual/selenium/chromedriver'

url = 'https://builtwith.com/ecommerce/united-states/shoes'

class_name = 'listItem__properties black default'

f = open('shoes_case1.txt', 'a')

browser = webdriver.Chrome(path)

browser.get(url)

lists = browser.find_elements_by_xpath("//table[@class='table table-striped tablePhone']/tbody/tr/td/img")

for item in lists:
    print item.get_attribute('src')
    source = str(item.get_attribute('src'))
    print
    f.write(source[source.index('=') + 1:] + '\n')
    # f.write(str(item.get_attribute('href')) + '\n')






# browser.get(url)