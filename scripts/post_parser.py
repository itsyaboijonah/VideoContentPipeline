from os.path import isfile

from bs4 import BeautifulSoup
import os, paths
from scripts.scraper import dump_to_pickle


class Reply:

    def __init__(self):
        self.author = None
        self.content = None
        self.likes = 0

    def set_author(self, author):
        self.author = author

    def set_content(self, content):
        self.content = content

    def set_likes(self, num_likes):
        self.likes = num_likes

    def flatten(self):
        output = [(self.author, self.content)]
        return output

    def get_author(self):
        return self.author

    def __str__(self):
        string = f"  Reply:\n" \
                 f"    Author: {self.author}\n" \
                 f"    Comment: {self.content}\n" \
                 f"    Likes: {self.likes}\n"
        return string


class Comment:

    def __init__(self):

        self.author = None
        self.content = None
        self.likes = 0
        self.num_replies = 0
        self.replies = None

    def set_author(self, author):
        self.author = author

    def set_content(self, content):
        self.content = content

    def set_likes(self, num_likes):
        self.likes = num_likes

    def set_num_replies(self, num_replies):
        self.num_replies = num_replies

    def add_reply(self, reply):
        if self.replies is None:
            self.replies = []
        self.replies.append(reply)

    def flatten(self):
        output = [(self.author, self.content)]
        if self.replies is None:
            return output
        for reply in self.replies:
            output += reply.flatten()
        return output

    def get_authors(self):
        authors = [self.author]
        if self.replies is None:
            return authors
        for reply in self.replies:
            authors.append(reply.get_author())
        return authors

    def __str__(self):
        string = f"Comment:\n" \
                 f"  Author: {self.author}\n" \
                 f"  Comment: {self.content}\n" \
                 f"  Likes: {self.likes}\n" \
                 f"  Number of Replies: {self.num_replies}\n"
        if not self.replies:
            return string
        for i in range(len(self.replies)):
            string += str(self.replies[i])
        return string


class Post:

    def __init__(self):
        self.title = None
        self.author = None
        self.content = None
        self.likes = 0
        self.num_comments = 0
        self.comments = None

    def set_title(self, title):
        self.title = title

    def set_author(self, author):
        self.author = author

    def set_content(self, content):
        self.content = content

    def set_likes(self, num_likes):
        self.likes = num_likes

    def set_num_comments(self, num_comments):
        self.num_comments = num_comments

    def add_comment(self, comment: Comment):
        if self.comments is None:
            self.comments = []
        self.comments.append(comment)

    def flatten(self):
        output = [(self.author, self.title)]
        # Checks if the post is in parts or one chunk, and appends accordingly
        if type(self.content) == list:
            for paragraph in self.content:
                output.append((self.author, paragraph))
        else:
            output.append((self.author, self.content))

        if self.comments is None:
            return output
        for comment in self.comments:
            output += comment.flatten()
        return output

    def get_authors(self):
        authors = [self.author]
        if self.comments is None:
            return authors
        for comment in self.comments:
            authors += comment.get_authors()
        return authors

    def __str__(self):
        string = f"Title: {self.title}\n" \
                 f"Author: {self.author}\n" \
                 f"Content: {self.content}\n" \
                 f"Likes: {self.likes}\n" \
                 f"Number of Comments: {self.num_comments}\n"
        if not self.comments:
            return string
        for i in range(len(self.comments)):
            string += str(self.comments[i])
        return string


class Parser:

    def __init__(self):
        self.post_id = None
        self.page_source = None
        self.post = None

    def load_page_source(self, batch_name, html_file):
        file = open(f"{paths.batch_scrapes_path}{batch_name}/html/{html_file}", "r")
        page_source = file.read()
        file.close()
        self.page_source = page_source
        self.post_id = html_file.split('.')[0]

    def parse_page_source(self):
        # Create Post object
        self.post = Post()

        # Page is structured as post, comments + replies
        soup = BeautifulSoup(self.page_source, 'html.parser')
        for a in soup.findAll('a', href=True):
            a.extract()

        # Parse post
        title = soup.find(class_="tit_area").find(class_="word-break").get_text(separator='. ')
        author = soup.find(class_="tit_area").find(class_="user").get_text(separator='. ')
        post_content = [str(text) for text in soup.find(class_="detail word-break").find("p").find_all(text=True) if text.strip()]
        likes = soup.find(class_="info").find(class_='like').get_text(separator='. ')
        num_comments = soup.find(class_="info").find(class_='comment').get_text(separator='. ')

        # Populates Post with parsed data
        self.post.set_title(title)
        self.post.set_author(author)
        self.post.set_content(post_content)
        self.post.set_likes(likes)
        self.post.set_num_comments(num_comments)

        # Parse comments and replies
        comments = soup.find(class_="topic_comments_wrap").find("ul").findChildren("li", recursive=False)
        if not comments:
            return

        for i in range(len(comments)):
            if comments[i].find(class_="blocked"):
                continue
            comment = Comment()
            comment_author = comments[i].find(class_="writer").find(class_="user").get_text(separator='. ')
            comment_content = comments[i].find(class_="detail").find("span").get_text(separator='. ')
            comment_likes = comments[i].find(class_="info").find(class_='like').get_text(separator='. ')
            comment_num_replies = comments[i].find(class_="info").find(class_='comment').get_text(separator='. ')
            comment.set_author(comment_author)
            comment.set_content(comment_content)
            comment.set_likes(comment_likes)
            comment.set_num_replies(comment_num_replies)

            replies = comments[i].find_all(class_="reply")[1].findChild("ul").findChildren("li", recursive=False)
            if not replies:
                self.post.add_comment(comment)
                continue
            for j in range(min(len(replies), 5)):
                if replies[j].find(class_="blocked"):
                    continue
                reply = Reply()
                reply_author = replies[j].find(class_="writer").find(class_="user").get_text(separator='. ')
                reply_content = replies[j].find(class_="detail").find("span").get_text(separator='. ')
                reply_likes = replies[j].find(class_="info").find(class_='like').get_text(separator='. ')
                reply.set_author(reply_author)
                reply.set_content(reply_content)
                reply.set_likes(reply_likes)
                comment.add_reply(reply)
            self.post.add_comment(comment)


def batch_parse(batch_name):
    print("Starting parser for batch parse...")
    parser = Parser()
    print("Done! Loading batch of files to parse...")
    path_to_batch = paths.batch_scrapes_path + batch_name
    files = [filename for filename in os.listdir(path_to_batch + "/html/") if
             isfile(f"{path_to_batch}/html/{filename}") and (filename[-4:] == "html")]
    print(files)
    for file in files:
        print(f"Parsing {file}...")
        parser.load_page_source(batch_name, file)
        parser.parse_page_source()
        dump_to_pickle(f"{path_to_batch}/parsed/{file.split('.')[0]}.pkl", parser.post)
        print(f"Done parsing {file}")
    print("Done batch parse!")


def parse_post(batch_name, html_filename):
    print("Starting parser for batch parse...")
    parser = Parser()
    print("Done! Loading batch of files to parse...")
    path_to_batch = paths.batch_scrapes_path + batch_name
    print(f"Parsing {html_filename}...")
    parser.load_page_source(batch_name, html_filename)
    parser.parse_page_source()
    dump_to_pickle(f"{path_to_batch}/parsed/{html_filename.split('.')[0]}.pkl", parser.post)
    print(f"Done parsing {html_filename}")
