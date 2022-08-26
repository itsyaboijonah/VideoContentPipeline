from moviepy.editor import *
from os import listdir, makedirs
from os.path import isfile, join
from moviepy.video.fx.fadeout import fadeout


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
    # set the FPS to 1
    video_clip.fps = 1
    video_clip.set_mask(video_clip.to_mask())
    print(video_clip.mask)
    # write the resulting video clip
    video_clip.write_videofile(output_path, codec="mpeg4")
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
        video_clips.append(add_image_to_audio(f"./posts/{post_id}/screenshots/{i}.png", f"./posts/{post_id}/tts_audio/{i}.mp3", f"./posts/{post_id}/videoclips/{i}.mp4"))
    if not isfile('./outro.mp4'):
        add_image_to_audio('./outro.jpeg', './outro.mp3', './outro.mp4')
    video_clips.append(VideoFileClip('./outro.mp4'))
    # video_clips.append(add_image_to_audio('./outro.jpeg', './outro.mp3', './outro.mp4'))
    # video_clips.append(VideoFileClip('./outro.mp4'))
    return video_clips


def generate_video(post_id):
    video_clips = generate_clips_with_audio(post_id)
    video_with_voiceover = concatenate_videoclips(video_clips, method="compose")
    video_voiceover = video_with_voiceover.audio
    # video_voiceover.write_audiofile(filename='./test.wav', fps=22000, codec='pcm_s16le', bitrate='50k')
    bgm = AudioFileClip("./bg-music/Ghostrifter-Official-Devyzed-Downtown-Glow.mp3")
    while bgm.duration < video_voiceover.duration:
        bgm = concatenate_audioclips([bgm, bgm])
    bgm = bgm.set_end(video_voiceover.duration + 6).audio_fadeout(3)

    new_video_audio = CompositeAudioClip([video_voiceover, bgm.volumex(0.2)])
    video_with_final_audio = video_with_voiceover.set_audio(new_video_audio)
    bg_video = VideoFileClip('./bg-video/bg-video.mp4')
    while bg_video.duration < video_with_final_audio.duration:
        bg_video = concatenate_videoclips([bg_video, bg_video])
    bg_video = bg_video.set_end(video_with_final_audio.duration)
    video_final = CompositeVideoClip([bg_video, video_with_final_audio.set_position('center')], use_bgclip=True)
    # video_final = fadeout(video_final, 2)
    video_final.write_videofile(f"./posts/{post_id}/video.mp4", codec='mpeg4')

