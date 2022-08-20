from moviepy.editor import *
from os import listdir, makedirs
from os.path import isfile, join


def add_image_to_audio(image_path, audio_path, output_path):
    """Create and save a video file to `output_path` after
    combining a static image that is located in `image_path`
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path, codec="mpeg4")
    return video_clip


def generate_video(post_id):
    num_images = len([filename for filename in listdir(f"./posts/{post_id}/screenshots/") if isfile(join(f"./posts/{post_id}/screenshots/", filename))])
    num_audio = len([filename for filename in listdir(f"./posts/{post_id}/tts_audio/") if isfile(join(f"./posts/{post_id}/tts_audio/", filename))])

    if num_images != num_audio:
        print("Missing one or more image/audio files. Please check the screenshots and tts_audio directories and try again.")
        exit()

    makedirs(f"./posts/{post_id}/videoclips", exist_ok=True)
    video_clips = []
    for i in range(num_images):
        video_clips.append(add_image_to_audio(f"./posts/{post_id}/screenshots/{i}.png", f"./posts/{post_id}/tts_audio/{i}.mp3", f"./posts/{post_id}/videoclips/{i}.mp4"))

    video_with_voiceover = concatenate_videoclips(video_clips, method="compose", bg_color=(0,0,0))
    video_voiceover = video_with_voiceover.audio
    lofi = AudioFileClip("./Ghostrifter-Official-Devyzed-Downtown-Glow.mp3")
    new_video_audio = CompositeAudioClip([video_voiceover, lofi.volumex(0.3)])
    video_final = video_with_voiceover.set_audio(new_video_audio)
    video_final.write_videofile(f"./posts/{post_id}/video.mp4")

