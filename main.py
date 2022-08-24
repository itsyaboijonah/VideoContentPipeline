from os import listdir
from os.path import isfile, isdir
import scraper
import post_parser
import screenshot_generator
import process_screenshots
import generate_audio
import generate_video
import multiprocessing as mp


if __name__ == "__main__":

    # TODO: Can create unused/already_used lists for each stage of the pipeline to assist with parallelization
    unused, already_used = [], []
    for post_id in listdir(f"./posts/"):
        if isdir(f"./posts/{post_id}/screenshots") and len(post_id) == 8:
            already_used.append(post_id)
        elif len(post_id) == 8:
            unused.append(post_id)

    new_post_ids = []  # scraper.scrape(already_used)
    unused.extend(new_post_ids)

    for post_id in unused[:1]:
        post_parser.parse(post_id)
        screenshot_generator.generate_screenshots(post_id)
        process_screenshots.process_screenshots(post_id)
        generate_audio.generate_audio(post_id)
        generate_video.generate_video(post_id)
