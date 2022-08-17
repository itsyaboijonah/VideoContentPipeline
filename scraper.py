import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import _pickle as pickle
import os

home_URL = "https://www.teamblind.com"
credentials_file = open("blind_credentials", "r")
credentials = credentials_file.readlines()
credentials = list(map(str.strip, credentials))
credentials_file.close()

def dump_to_pickle(filename, data_to_dump):
    file = open(filename, 'wb')
    pickle.dump(data_to_dump, file)
    file.close()


def load_from_pickle(filename):
    file = open(filename, "rb")
    data = pickle.load(file)
    file.close()
    return data


class Scraper:

    def __init__(self):
        caps = DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"  # interactive
        self.driver = webdriver.Chrome(desired_capabilities=caps)
        self.hot_posts_urls = None
        self.is_logged_in = False
        self.login()

    def login(self):
        self.driver.get(home_URL)
        time.sleep(2)
        elem = self.driver.find_element(By.CLASS_NAME, "btn_logIn")
        elem.click()
        elem = self.driver.find_element(By.XPATH,
                                   "/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div/div/div[2]/div[1]/ul/li[1]/div/input")
        elem.send_keys(credentials[0])
        time.sleep(2)
        elem = self.driver.find_element(By.XPATH,
                                   "/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div/div/div[2]/div[1]/ul/li[2]/div/input")
        elem.send_keys(credentials[1])
        time.sleep(2)
        elem = self.driver.find_element(By.XPATH,
                                   "/html/body/div[1]/div/main/div[3]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[1]/button")
        elem.click()
        time.sleep(2)
        self.check_login()

    def check_login(self):
        self.driver.get(home_URL)
        if self.driver.find_elements(By.CLASS_NAME, "btn_logIn"):
            self.is_logged_in = False
            return False
        else:
            self.is_logged_in = True
            return True

    def quit(self):
        self.driver.quit()

    def print_hot_posts(self):
        for key in self.hot_posts_urls.keys():
            print(key, self.hot_posts_urls[key])

    def pull_hot_posts(self):
        self.driver.get("https://www.teamblind.com/topics/Industries/Tech")
        time.sleep(3)
        elem = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/section/div/div/div[2]/ul")
        items = elem.find_elements(By.CLASS_NAME, "word-break")
        self.hot_posts_urls = {}
        for item in items:
            # https://stackoverflow.com/questions/19664253/selenium-how-to-get-the-content-of-href-within-some-targeted-class
            url = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            post_key = url[-8:]
            self.hot_posts_urls[post_key] = url

    def pull_post_and_comments(self, post_url):
        if not self.is_logged_in:
            self.login()
        self.driver.get(post_url)
        time.sleep(2)
        elem = self.driver.find_element(By.CLASS_NAME, "topic_comments_wrap").find_element(By.TAG_NAME, "ul")

        more_replies = elem.find_elements(By.CLASS_NAME, "btn_more")

        while more_replies:
            for i in range(len(more_replies)):
                time.sleep(2)
                self.driver.execute_script("arguments[0].click();", more_replies[i])
            time.sleep(2)
            more_replies = elem.find_elements(By.CLASS_NAME, "btn_more")

        expanded_page_source = self.driver.page_source
        post_key = post_url[-8:]
        os.makedirs(f"./posts/{post_key}", exist_ok=True)
        file = open(f"./posts/{post_key}/page_source.html", "w")
        file.write(expanded_page_source)
        file.close()


if __name__ == "__main__":
    print("Starting scraper...")
    main_driver = Scraper()
    print("Scraper initialized! Logged in is " + str(main_driver.is_logged_in))
    # print("Pulling hot posts in the Tech category...")
    # main_driver.pull_hot_posts()
    # print("Done! The following URLs were pulled:")
    # main_driver.print_hot_posts()
    # main_driver.pull_post_and_comments("https://www.teamblind.com/post/Really-annoyed-with-my-new-manager-ex-Amazon-Cw3SvZy3")
    # main_driver.quit()
