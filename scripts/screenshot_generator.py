import time
import paths
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from selenium.webdriver.chrome.options import Options


def generate_screenshots(post_id):
    os.makedirs(f"{paths.posts_path}{post_id}/screenshots", exist_ok=True)
    cur_screenshot = 0

    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"  # interactive
    opt = Options()
    opt.add_extension(f"{paths.project_path}/4.9.57_0.crx")
    driver = webdriver.Chrome(desired_capabilities=caps, options=opt)

    driver.get(f"file://{paths.posts_path}{post_id}/page_source.html")
    time.sleep(2)
    # post_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/section/div/div/div[2]/section/div[1]")
    title = driver.find_element(By.CLASS_NAME, "article.seo").find_element(By.CLASS_NAME, "tit_area")
    title.screenshot(f"{paths.posts_path}{post_id}/screenshots/{cur_screenshot}.png")
    cur_screenshot += 1

    post = driver.find_element(By.CLASS_NAME, "article.seo").find_element(By.CLASS_NAME, "detail.word-break").find_element(By.ID, "contentArea")
    post.screenshot(f"{paths.posts_path}{post_id}/screenshots/{cur_screenshot}.png")
    cur_screenshot += 1

    attachment = driver.find_element(By.CLASS_NAME, "article.seo").find_element(By.CLASS_NAME, "detail.word-break").find_elements(By.CLASS_NAME, "attach")
    if attachment:
        attachment_src = attachment[0].find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "img").get_attribute("src")
        driver.get(attachment_src)
        driver.find_element(By.TAG_NAME, "img").screenshot(f"{paths.posts_path}{post_id}/screenshots/{cur_screenshot}.png")
        driver.back()
        cur_screenshot += 1

    comments = driver.find_element(By.CLASS_NAME, "topic_comments_wrap").find_element(By.TAG_NAME, "ul").find_elements(By.XPATH, "./child::*")
    for i in range(len(comments)):
        if comments[i].find_elements(By.CLASS_NAME, "blocked"):
            continue
        comments[i].find_element(By.CLASS_NAME, "content").screenshot(f"{paths.posts_path}{post_id}/screenshots/{cur_screenshot}.png")
        cur_screenshot += 1
        replies = comments[i].find_elements(By.CLASS_NAME, "reply")[1].find_element(By.TAG_NAME, "ul").find_elements(By.XPATH, "./child::*")
        for j in range(min(len(replies), 5)):
            if replies[j].find_elements(By.CLASS_NAME, "blocked"):
                continue
            replies[j].find_element(By.CLASS_NAME, "content").screenshot(f"{paths.posts_path}{post_id}/screenshots/{cur_screenshot}.png")
            cur_screenshot += 1
