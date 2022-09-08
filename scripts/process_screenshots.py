from PIL import Image
from os import listdir
from os.path import isfile, join
import paths

resize_factor = 1.8


def process_screenshots(post_id):
    # Gets list of png filenames to edit
    files = [filename for filename in listdir(f"{paths.posts_path}{post_id}/screenshots/") if isfile(join(f"{paths.posts_path}{post_id}/screenshots/", filename)) and (filename[-3:] == "png")]

    # Add padding to each png and save the result
    for filename in files:
        image = Image.open(f"{paths.posts_path}{post_id}/screenshots/{filename}")
        rgb = image.convert('RGB')
        r, g, b = rgb.getpixel((1, 1))
        width, height = image.size
        new_width = width + 40
        if filename == '1.png':
            processed_image = Image.new('RGB', (new_width, height + 40), (r, g, b))
            processed_image.paste(image, (20, 20))
        else:
            processed_image = Image.new('RGB', (new_width, height), (r, g, b))
            processed_image.paste(image, (20, 0))
        if filename == '0.png':
            width, height = processed_image.size
            temp_image = processed_image.crop((0, 20, width, height))
            width, height = temp_image.size
            processed_image = Image.new('RGB', (width, height+20), (r, g, b))
            processed_image.paste(temp_image, (0, 0))
        image.close()
        resized_image = processed_image.resize((int(round(resize_factor*processed_image.width)), int(round(resize_factor*processed_image.height))), Image.ANTIALIAS)
        resized_image.save(f"{paths.posts_path}{post_id}/screenshots/{filename}", "png")
