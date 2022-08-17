from bs4 import BeautifulSoup
import os


def load_page_source(post_key):
    file = open(f"./posts/{post_key}/page_source.html", "r")
    page_source = file.read()
    file.close()
    print(page_source)


class Parser:

    def __init__(self):


if __name__ == "__main__":
    print("Starting parser...")
    load_page_source("Cw3SvZy3")