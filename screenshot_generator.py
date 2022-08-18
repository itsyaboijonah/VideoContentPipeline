import time
from selenium import webdriver
from selenium.webdriver.common.by import By

post_id = "Cw3SvZy3"
path_to_project = "/Users/jonah/PycharmProjects/VideoContentPipeline"

driver = webdriver.Chrome()

driver.get(f"file://{path_to_project}/posts/{post_id}/page_source.html")
time.sleep(2)
# post_elem = driver.find_element(By.XPATH, "/html/body/div[1]/div/main/div[2]/section/div/div/div[2]/section/div[1]")
post_elem = driver.find_element(By.CLASS_NAME, "article.seo")
post_elem.screenshot(f"./posts/{post_id}/post.png")

comments = driver.find_element(By.CLASS_NAME, "topic_comments_wrap").find_element(By.TAG_NAME, "ul").find_elements(By.XPATH, "./child::*")
for i in range(len(comments)):
    comments[i].find_element(By.CLASS_NAME, "content").screenshot(f"./posts/{post_id}/comment{i+1}.png")
    replies = comments[i].find_elements(By.CLASS_NAME, "reply")[1].find_element(By.TAG_NAME, "ul").find_elements(By.XPATH, "./child::*")
    for j in range(min(len(replies), 5)):
        replies[j].find_element(By.CLASS_NAME, "content").screenshot(f"./posts/{post_id}/reply{i+1}-{j+1}.png")
