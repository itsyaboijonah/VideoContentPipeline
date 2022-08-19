import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os

post_id = "Cw3SvZy3"
path_to_project = "/Users/jonah/PycharmProjects/VideoContentPipeline"
os.makedirs(f"./posts/{post_id}/screenshots", exist_ok=True)
cur_screenshot = 0

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"  # interactive
driver = webdriver.Chrome(desired_capabilities=caps)

driver.get(f"file://{path_to_project}/posts/{post_id}/page_source.html")
time.sleep(2)
# post_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/section/div/div/div[2]/section/div[1]")
title = driver.find_element(By.CLASS_NAME, "article.seo").find_element(By.CLASS_NAME, "tit_area")
title.screenshot(f"./posts/{post_id}/screenshots/{cur_screenshot}.png")
cur_screenshot += 1

post = driver.find_element(By.CLASS_NAME, "article.seo").find_element(By.CLASS_NAME, "detail.word-break")
post.screenshot(f"./posts/{post_id}/screenshots/{cur_screenshot}.png")
cur_screenshot += 1

comments = driver.find_element(By.CLASS_NAME, "topic_comments_wrap").find_element(By.TAG_NAME, "ul").find_elements(By.XPATH, "./child::*")
for i in range(len(comments)):
    comments[i].find_element(By.CLASS_NAME, "content").screenshot(f"./posts/{post_id}/screenshots/{cur_screenshot}.png")
    cur_screenshot += 1
    replies = comments[i].find_elements(By.CLASS_NAME, "reply")[1].find_element(By.TAG_NAME, "ul").find_elements(By.XPATH, "./child::*")
    for j in range(min(len(replies), 5)):
        replies[j].find_element(By.CLASS_NAME, "content").screenshot(f"./posts/{post_id}/screenshots/{cur_screenshot}.png")
        cur_screenshot += 1
