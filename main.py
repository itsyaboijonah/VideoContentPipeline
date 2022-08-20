from os import listdir
from os.path import isfile, join
import scraper
import parser
import screenshot_generator
import process_screenshots
import generate_audio
import generate_video

if __name__ == "__main__":

    already_used = [post_id for post_id in listdir(f"./posts/") if
             not isfile(join(f"./posts/{post_id}/screenshots/", post_id)) and len(post_id) == 8]
    post_id = scraper.scrape(already_used)
    parser.parse(post_id)
    screenshot_generator.generate_screenshots(post_id)
    process_screenshots.process_screenshots(post_id)
    generate_audio.generate_audio(post_id)
    generate_video.generate_video(post_id)
