from scripts.post_parser import Post, Comment, Reply
from scripts.scraper import load_from_pickle
from statistics import mean
import paths
import nltk


# TODO: Use some NLP techniques to generate good features for video creation model

class ReplyData(Reply):

    def __init__(self, reply=None):
        super().__init__()
        self.reply_length = 0
        if reply:
            self.author = reply.author
            self.content = reply.content
            self.likes = reply.likes
            self.calculate()

    def calculate(self):
        self.update_reply_length()

    def update_reply_length(self):
        self.reply_length = len(self.content)


class CommentData(Comment):

    def __init__(self, comment=None):
        super().__init__()
        self.comment_length = 0
        self.longest_reply = 0
        self.shortest_reply = 0
        self.average_reply_len = 0
        if comment:
            self.author = comment.author
            self.content = comment.content
            self.likes = comment.likes
            self.num_replies = comment.num_replies
            self.replies = list(map(lambda x: ReplyData(x), comment.replies)) if comment.replies else None
            self.calculate()

    def calculate(self):
        self.update_comment_length()
        self.update_longest_reply()
        self.update_shortest_reply()
        self.update_average_reply_len()

    def update_comment_length(self):
        self.comment_length = len(self.content)

    def update_longest_reply(self):
        if self.replies:
            self.longest_reply = max(x.reply_length for x in self.replies)

    def update_shortest_reply(self):
        if self.replies:
            self.shortest_reply = min(x.reply_length for x in self.replies)

    def update_average_reply_len(self):
        if self.replies:
            self.average_reply_len = mean(x.reply_length for x in self.replies)


class PostData(Post):

    def __init__(self, post_id=None):
        super().__init__()
        self.post_id = None
        self.post_length = 0
        self.longest_comment = 0
        self.shortest_comment = 0
        self.average_comment_len = 0
        if post_id:
            self.load_post_data(post_id)
            self.calculate()

    def calculate(self):
        self.update_post_length()
        self.update_longest_comment()
        self.update_shortest_comment()
        self.update_average_comment_len()

    def update_post_length(self):
        self.post_length = len(self.content)

    def update_longest_comment(self):
        self.longest_comment = max(x.comment_length for x in self.comments)

    def update_shortest_comment(self):
        self.shortest_comment = min(x.comment_length for x in self.comments)

    def update_average_comment_len(self):
        self.average_comment_len = mean(x.comment_length for x in self.comments)

    def load_post_data(self, post_id):
        post_pkl = load_from_pickle(f"{paths.posts_path}{post_id}/parsed_post.pkl")
        self.post_id = post_id
        self.title = post_pkl.title
        self.author = post_pkl.author
        self.content = post_pkl.content
        self.likes = post_pkl.likes
        self.num_comments = post_pkl.num_comments
        self.comments = list(map(lambda x: CommentData(x), post_pkl.comments)) if post_pkl.comments else None

