from os import listdir, makedirs
from os.path import isfile, isdir
import shutil, paths
from scripts import scraper, post_parser, screenshot_generator, process_screenshots, generate_audio, generate_video

num_posts_to_process = 1

def parse_post(post_id):
    post_parser.parse(post_id)


def generate_post_screenshots(post_id):
    screenshot_generator.generate_screenshots(post_id)


def process_post_screenshots(post_id):
    process_screenshots.process_screenshots(post_id)


def generate_post_audio(post_id):
    generate_audio.generate_audio(post_id)


def generate_post_video(post_id):
    generate_video.generate_video(post_id)


def archive_post(post_id):
    makedirs(paths.archives_path, exist_ok=True)
    shutil.move(f'{paths.posts_path}{post_id}', f'{paths.archives_path}{post_id}')


def post_pipeline(post_id):
    parse_post(post_id)
    generate_post_screenshots(post_id)
    process_post_screenshots(post_id)
    generate_post_audio(post_id)
    generate_post_video(post_id)
    archive_post(post_id)


if __name__ == "__main__":

    # TODO: Can create unused/already_used lists for each stage of the pipeline to assist with parallelization
    # TODO: Need to create way of ranking/analyzing posts (num comments, num replies, avg length of each, etc) so that good posts can be prioritized
    # TODO: Enhance code documentation
    # TODO: Add logging
    unused, already_used = [], []
    for post_id in listdir(f"{paths.posts_path}"):
        if isdir(f"{paths.posts_path}{post_id}/screenshots") and len(post_id) == 8:
            already_used.append(post_id)
        elif len(post_id) == 8:
            unused.append(post_id)

    new_post_ids = scraper.scrape(already_used, 5)
    unused.extend(new_post_ids)

    for post_id in unused[:num_posts_to_process]:
        post_pipeline(post_id)
        archive_post(post_id)
