import operator
import os
from os.path import isfile
import paths
from scripts.scraper import load_from_pickle


def generate_post_rankings(batch_name):
    path_to_batch = paths.batch_scrapes_path + batch_name
    files = [filename for filename in os.listdir(path_to_batch + "/data/") if
             isfile(f"{path_to_batch}/data/{filename}") and (filename[-3:] == "pkl")]
    batch_data = []
    for file in files:
        batch_data.append(load_from_pickle(f"{path_to_batch}/data/{file}"))
    batch_data.sort(key=operator.attrgetter('total_likes'), reverse=True)

    for i, data in enumerate(batch_data):
        print(f"Rank {i+1}: {data.post_id}, Total Likes: {data.total_likes}")

    return list(map(lambda x: x.post_id, batch_data))