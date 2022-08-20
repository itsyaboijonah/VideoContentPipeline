import scraper
import parser
import screenshot_generator
import process_screenshots
import generate_audio
import generate_video

if __name__ == "__main__":

    post_id = scraper.scrape()
    parser.parse(post_id)
    screenshot_generator.generate_screenshots(post_id)
    process_screenshots.process_screenshots(post_id)
    generate_audio.generate_audio(post_id)
    generate_video.generate_video(post_id)
