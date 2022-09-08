import os
from os import listdir, makedirs
from os.path import isfile, isdir
import shutil, paths
from scripts import scraper, post_parser, screenshot_generator, process_screenshots, generate_audio, generate_video, generate_post_data, generate_post_rankings

num_posts_to_process = 5


def parse_post(post_id):
    post_parser.parse(post_id)


def generate_post_screenshots(batch_name, post_id):
    screenshot_generator.generate_screenshots(batch_name, post_id)


def process_post_screenshots(post_id):
    process_screenshots.process_screenshots(post_id)


def generate_post_audio(batch_name, post_id):
    generate_audio.generate_audio(batch_name, post_id)


def generate_post_video(post_id):
    generate_video.generate_video(post_id)


def archive_post(post_id):
    makedirs(paths.archives_path, exist_ok=True)
    shutil.move(f'{paths.posts_path}{post_id}', f'{paths.archives_path}{post_id}')


def post_pipeline(batch_name, post_id):
    generate_post_screenshots(batch_name, post_id)
    process_post_screenshots(post_id)
    generate_post_audio(batch_name, post_id)
    generate_post_video(post_id)
    archive_post(post_id)


if __name__ == "__main__":

    # TODO: Enhance code documentation
    # TODO: Add logging

    batch_name = scraper.scrape()
    post_parser.batch_parse(batch_name)
    generate_post_data.batch_analyze(batch_name)
    ranked_post_ids = generate_post_rankings.generate_post_rankings(batch_name)

    for post_id in ranked_post_ids[:num_posts_to_process]:
        makedirs(f"paths.posts_path{post_id}", exist_ok=True)
        post_pipeline(batch_name, post_id)
