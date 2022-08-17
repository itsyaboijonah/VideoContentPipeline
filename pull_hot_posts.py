import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import _pickle as pickle

# https://stackoverflow.com/questions/46322165/dont-wait-for-a-page-to-load-using-selenium-in-python
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  #  interactive
driver = webdriver.Chrome(desired_capabilities=caps)
driver.get("https://www.teamblind.com")
time.sleep(2)
elem = driver.find_element(By.CLASS_NAME, "btn_logIn")
elem.click()
elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div/div/div[2]/div[1]/ul/li[1]/div/input")
elem.send_keys("jonah.nimijean@citi.com")
time.sleep(2)
elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div/div/div[2]/div[1]/ul/li[2]/div/input")
elem.send_keys("Eljoh_9799")
time.sleep(2)
elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/button")
elem.click()
time.sleep(2)
driver.get("https://www.teamblind.com/topics/Industries/Tech")
time.sleep(3)
elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/section/div/div/div[2]/ul")
items = elem.find_elements(By.CLASS_NAME, "word-break")

hot_post_urls = {}
for item in items:
    print(item.text)
    # https://stackoverflow.com/questions/19664253/selenium-how-to-get-the-content-of-href-within-some-targeted-class
    url = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    print(url)
    post_key = url[-8:]
    hot_post_urls[post_key] = url

print(hot_post_urls.values())

file = open("hot_post_urls.pkl", 'wb')
pickle.dump(hot_post_urls, file)
file.close()

# elem.clear()
# assert "No results found." not in driver.page_source
driver.close()