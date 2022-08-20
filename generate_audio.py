import gtts
from parser import Post, Comment
from scraper import load_from_pickle
import sox
from mutagen.mp3 import MP3
import os


def generate_audio(post_id):
    post_content = load_from_pickle(f"./posts/{post_id}/parsed_post.pkl").flatten()
    os.makedirs(f"./posts/{post_id}/tts_audio", exist_ok=True)
    for i, text in enumerate(post_content):
        print(f"Processing audio sample #{i}...")
        print(f"Text: {text}")
        tts = gtts.gTTS(text, lang="en-uk")
        tts.save(f"./posts/{post_id}/tts_audio/{i}_original.mp3")
        tfm = sox.Transformer()
        sample_length = MP3(f"./posts/{post_id}/tts_audio/{i}_original.mp3").info.length
        print(f"Sample length: {sample_length}")
        if sample_length > 1.8:
            tfm.tempo(1.2)
            tfm.silence(min_silence_duration=0.5)
        tfm.pad(end_duration=0.5)
        tfm.build_file(f'./posts/{post_id}/tts_audio/{i}_original.mp3', f'./posts/{post_id}/tts_audio/{i}.mp3')
        print("Done! Removing intermediary mp3 file...")
        os.remove(f"./posts/{post_id}/tts_audio/{i}_original.mp3")
        print(f"Done rendering audio sample #{i}!")
