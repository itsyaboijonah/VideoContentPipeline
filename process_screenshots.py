from PIL import Image
from os import listdir
from os.path import isfile, join


def process_screenshots(post_id):
    # Gets list of png filenames to edit
    files = [filename for filename in listdir(f"./posts/{post_id}/screenshots/") if isfile(join(f"./posts/{post_id}/screenshots/", filename)) and (filename[-3:] == "png")]

    # Add padding to each png and save the result
    for filename in files:
        image = Image.open(f"./posts/{post_id}/screenshots/{filename}")
        rgb = image.convert('RGB')
        r, g, b = rgb.getpixel((1, 1))
        width, height = image.size
        new_width = width + 40
        processed_image = Image.new('RGB', (new_width, height), (r, g, b))
        processed_image.paste(image, (20, 0))
        if filename == '0.png':
            width, height = processed_image.size
            temp_image = processed_image.crop((0, 20, width, height))
            width, height = temp_image.size
            processed_image = Image.new('RGB', (width, height+20), (r, g, b))
            processed_image.paste(temp_image, (0, 0))
        image.close()
        processed_image.save(f"./posts/{post_id}/screenshots/{filename}", "png")
