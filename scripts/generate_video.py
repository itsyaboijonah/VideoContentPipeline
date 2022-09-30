from moviepy.editor import *
from os import listdir, makedirs
from os.path import isfile, join
import re, random, paths

from moviepy.video.fx.mirror_x import mirror_x


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
    num_images = len([filename for filename in listdir(f"{paths.posts_path}{post_id}/screenshots/") if isfile(join(f"{paths.posts_path}{post_id}/screenshots/", filename))])
    num_audio = len([filename for filename in listdir(f"{paths.posts_path}{post_id}/tts_audio/") if isfile(join(f"{paths.posts_path}{post_id}/tts_audio/", filename))])

    if num_images != num_audio:
        print("Missing one or more image/audio files. Please check the screenshots and tts_audio directories and try again.")
        exit()

    makedirs(f"{paths.posts_path}{post_id}/videoclips", exist_ok=True)

    video_clips = []
    for i in range(num_images):
        video_clips.append(add_image_to_audio(f"{paths.posts_path}{post_id}/screenshots/{i}.png", f"{paths.posts_path}{post_id}/tts_audio/{i}.mp3", f"{paths.posts_path}{post_id}/videoclips/{i}.avi"))
    return video_clips


def load_video_clips(post_id):
    filenames = sorted([filename for filename in listdir(f"{paths.posts_path}{post_id}/videoclips/")], key=lambda string: int(re.search(r'\d+', string).group()))
    path_filenames = list(map(lambda filename: f"{paths.posts_path}{post_id}/videoclips/{filename}", filenames))
    # path_filenames.append('../outro.mp4')
    return [VideoFileClip(filename) for filename in path_filenames]


def generate_video_from_clips(post_id):
    video_clips = load_video_clips(post_id)
    # Pad the final clip
    video_clips[-1] = video_clips[-1].set_end(video_clips[-1].end + 2).set_duration(video_clips[-1].duration + 2).set_audio(CompositeAudioClip([video_clips[-1].audio, AudioClip(lambda t: 0, duration=2)]))
    video_with_voiceover = concatenate_videoclips(video_clips, method="compose")
    video_voiceover = video_with_voiceover.audio

    # Handles adding the background music
    available_bgm = [filename for filename in listdir(f"{paths.bg_music_path}") if
                      isfile(join(paths.bg_music_path, filename)) and filename[-3:] == "wav"]
    bgm = AudioFileClip(f"{paths.bg_music_path}{str(random.choice(available_bgm))}")
    while bgm.duration < video_voiceover.duration:
        bgm = concatenate_audioclips([bgm, bgm])
    bgm = bgm.set_end(video_voiceover.duration + 2)

    new_video_audio = CompositeAudioClip([video_voiceover, bgm.volumex(0.2)])
    video_with_final_audio = video_with_voiceover.set_audio(new_video_audio)
    bg_video = VideoFileClip(f'{paths.bg_video_path}bg-video{random.randint(0,5)}.mp4')
    bg_video = bg_video.rotate(90)
    if random.randint(0, 2):
        bg_video = mirror_x(bg_video)
    while bg_video.duration < video_with_final_audio.duration:
        bg_video = concatenate_videoclips([bg_video, bg_video])
    video_final = CompositeVideoClip([bg_video, video_with_final_audio.set_position('center')], use_bgclip=True)
    # video_final = fadeout(video_final, 2)
    # Tuned codec and bitrate for better quality/filesize ratio
    makedirs(f"{paths.output_videos_path}", exist_ok=True)
    video_final.write_videofile(f"{paths.output_videos_path}{post_id}.mp4", codec='libx264', bitrate='3000k')


def generate_video(post_id):
    generate_clips_with_audio(post_id)
    generate_video_from_clips(post_id)