from bs4 import BeautifulSoup
import os
from scraper import dump_to_pickle

post_id = "Cw3SvZy3"


class Comment:

    def __init__(self):
        self.content = None
        self.replies = None

    def set_content(self, content):
        self.content = content

    def add_reply(self, reply):
        if self.replies is None:
            self.replies = []
        self.replies.append(reply)

    def flatten(self):
        output = [self.content]
        for reply in self.replies:
            output.append(reply)
        return output

    def __str__(self):
        string = f"Comment: {self.content}\nReplies:\n"
        for i in range(len(self.replies)):
            string += f"    - {self.replies[i]}\n"
        return string


class Post:

    def __init__(self):
        self.title = None
        self.content = None
        self.comments = None

    def set_title(self, title):
        self.title = title

    def set_content(self, content):
        self.content = content

    def add_comment(self, comment: Comment):
        if self.comments is None:
            self.comments = []
        self.comments.append(comment)

    def flatten(self):
        output = [self.title, self.content]
        for comment in self.comments:
            output += comment.flatten()
        return output

    def __str__(self):
        string = f"Title: {self.title}\n"
        string += f"Content: {self.content}\n"
        for i in range(len(self.comments)):
            string += str(self.comments[i])
        return string


class Parser:

    def __init__(self):
        self.post_id = None
        self.page_source = None
        self.post = None

    def load_page_source(self, post_id):
        file = open(f"./posts/{post_id}/page_source.html", "r")
        page_source = file.read()
        file.close()
        self.page_source = page_source
        self.post_id = post_id

    def parse_page_source(self):
        # Create Post object
        self.post = Post()

        # Page is structured as post, comments + replies
        soup = BeautifulSoup(self.page_source, 'html.parser')

        # Parse post
        title = soup.find(class_="tit_area").find(class_="word-break").get_text()
        post_content = soup.find(class_="detail word-break").find("p").get_text()

        # Populates Post with parsed data
        self.post.set_title(title)
        self.post.set_content(post_content)

        # Parse comments and replies
        comments = soup.find(class_="topic_comments_wrap").find("ul").findChildren("li", recursive=False)

        for i in range(len(comments)):
            comment = Comment()
            comment.set_content(comments[i].find(class_="detail").find("span").get_text())
            replies = comments[i].find_all(class_="reply")[1].findChild("ul").findChildren("li", recursive=False)
            for j in range(min(len(replies), 5)):
                comment.add_reply(replies[j].find(class_="detail").find("span").get_text())
            self.post.add_comment(comment)


if __name__ == "__main__":
    print("Starting parser...")
    parser = Parser()
    print("Done! Loading page source...")
    parser.load_page_source(post_id)
    print(f"Page source loaded for {post_id}. Parsing...")
    parser.parse_page_source()
    print(f"Done! Parsed Post object has been created:")
    print(str(parser.post))
    print("Dumping Post to pickle...")
    dump_to_pickle(f"./posts/{post_id}/parsed_post.pkl", parser.post)
    print("Done!")
