import pickle

file = open("hot_post_urls.pkl", "rb")
hot_posts_urls = pickle.load(file)

for key in hot_posts_urls.keys():
    print(key, hot_posts_urls[key])

