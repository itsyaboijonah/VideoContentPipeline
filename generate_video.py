from moviepy.editor import *
from os import listdir, makedirs
from os.path import isfile, join
import re
import random


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
    video_clip.duration = audio_clip.duration + 0.5
    if video_clip.duration < 1:
        video_clip.duration = 1
    # set the FPS to 1
    video_clip.fps = 1
    video_clip = video_clip.add_mask()
    # write the resulting video clip
    video_clip.write_videofile(output_path, codec="png")
    return video_clip


def generate_clips_with_audio(post_id):
    num_images = len([filename for filename in listdir(f"./posts/{post_id}/screenshots/") if isfile(join(f"./posts/{post_id}/screenshots/", filename))])
    num_audio = len([filename for filename in listdir(f"./posts/{post_id}/tts_audio/") if isfile(join(f"./posts/{post_id}/tts_audio/", filename))])

    if num_images != num_audio:
        print("Missing one or more image/audio files. Please check the screenshots and tts_audio directories and try again.")
        exit()

    makedirs(f"./posts/{post_id}/videoclips", exist_ok=True)

    video_clips = []
    for i in range(num_images):
        video_clips.append(add_image_to_audio(f"./posts/{post_id}/screenshots/{i}.png", f"./posts/{post_id}/tts_audio/{i}.mp3", f"./posts/{post_id}/videoclips/{i}.avi"))
    # if not isfile('./outro.mp4'):
    #     add_image_to_audio('./outro.jpeg', './outro.mp3', './outro.mp4')
    # video_clips.append(VideoFileClip('./outro.mp4'))
    # video_clips.append(add_image_to_audio('./outro.jpeg', './outro.mp3', './outro.mp4'))
    # video_clips.append(VideoFileClip('./outro.mp4'))
    return video_clips


def load_video_clips(post_id):
    filenames = sorted([filename for filename in listdir(f"./posts/{post_id}/videoclips/")], key=lambda string: int(re.search(r'\d+', string).group()))
    path_filenames = list(map(lambda filename: f"./posts/{post_id}/videoclips/{filename}", filenames))
    # path_filenames.append('./outro.mp4')
    return [VideoFileClip(filename) for filename in path_filenames]


def generate_video_from_clips(post_id):
    video_clips = load_video_clips(post_id)
    # Pad the final clip
    video_clips[-1] = video_clips[-1].set_end(video_clips[-1].end + 2).set_duration(video_clips[-1].duration + 2).set_audio(CompositeAudioClip([video_clips[-1].audio, AudioClip(lambda t: 0, duration=2)]))
    video_with_voiceover = concatenate_videoclips(video_clips, method="compose", padding=0.5)
    video_voiceover = video_with_voiceover.audio
    # video_voiceover.write_audiofile(filename='./test.wav', fps=22000, codec='pcm_s16le', bitrate='50k')
    bgm = AudioFileClip("./bg-music/Ghostrifter-Official-Devyzed-Downtown-Glow.mp3")
    while bgm.duration < video_voiceover.duration:
        bgm = concatenate_audioclips([bgm, bgm])
    bgm = bgm.set_end(video_voiceover.duration + 2)

    new_video_audio = CompositeAudioClip([video_voiceover, bgm.volumex(0.2)])
    video_with_final_audio = video_with_voiceover.set_audio(new_video_audio)
    bg_video = VideoFileClip(f'./bg-video/bg-video{random.randint(0,6)}.mp4')
    bg_video = bg_video.rotate(90)
    if random.randint(0, 2):
        bg_video = bg_video.mirror_x()
    while bg_video.duration < video_with_final_audio.duration:
        bg_video = concatenate_videoclips([bg_video, bg_video])
    video_final = CompositeVideoClip([bg_video, video_with_final_audio.set_position('center')], use_bgclip=True)
    # video_final = fadeout(video_final, 2)
    # Tuned codec and bitrate for better quality/filesize ratio
    makedirs(f"./videos", exist_ok=True)
    video_final.write_videofile(f"./videos/{post_id}.mp4", codec='libx264', bitrate='3000k')


def generate_video(post_id):
    generate_clips_with_audio(post_id)
    generate_video_from_clips(post_id)