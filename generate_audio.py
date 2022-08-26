# import gtts
from post_parser import Post, Comment
from scraper import load_from_pickle
import sox
from mutagen.mp3 import MP3
import os
import boto3
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

session = Session(profile_name='polly_tts_user')
polly = session.client('polly', region_name='us-east-2')


def render(text_to_render, output_filename):
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text_to_render, OutputFormat="mp3",
                                            VoiceId="Matthew")
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        sys.exit(-1)

    # Access the audio stream from the response
    if "AudioStream" in response:
        # Note: Closing the stream is important because the service throttles on the
        # number of parallel connections. Here we are using contextlib.closing to
        # ensure the close method of the stream object will be called automatically
        # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
               try:
                # Open a file for writing the output as a binary stream
                    with open(output_filename, "wb") as file:
                       file.write(stream.read())
               except IOError as error:
                  # Could not write to file, exit gracefully
                  print(error)
                  sys.exit(-1)

    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)


def generate_audio(post_id):
    post_content = load_from_pickle(f"./posts/{post_id}/parsed_post.pkl").flatten()
    os.makedirs(f"./posts/{post_id}/tts_audio", exist_ok=True)
    for i, text in enumerate(post_content):
        print(f"Processing audio sample #{i}...")
        print(f"Text: {text}")
        render(text, f"./posts/{post_id}/tts_audio/{i}.mp3")
        # tfm = sox.Transformer()
        # sample_length = MP3(f"./posts/{post_id}/tts_audio/{i}_original.mp3").info.length
        # print(f"Sample length: {sample_length}")
        # # if sample_length > 1.8:
        # #     tfm.tempo(1.2)
        # #     tfm.silence(min_silence_duration=0.5)
        # tfm.pad(end_duration=0.5)
        # tfm.build_file(f'./posts/{post_id}/tts_audio/{i}_original.mp3', f'./posts/{post_id}/tts_audio/{i}.mp3')
        # print("Done! Removing intermediary mp3 file...")
        # os.remove(f"./posts/{post_id}/tts_audio/{i}_original.mp3")
        print(f"Done rendering audio sample #{i}!")

# Old implementation using gtts instead of AWS polly
# def generate_audio(post_id):
#     post_content = load_from_pickle(f"./posts/{post_id}/parsed_post.pkl").flatten()
#     os.makedirs(f"./posts/{post_id}/tts_audio", exist_ok=True)
#     for i, text in enumerate(post_content):
#         print(f"Processing audio sample #{i}...")
#         print(f"Text: {text}")
#         tts = gtts.gTTS(text, lang="en-uk")
#         tts.save(f"./posts/{post_id}/tts_audio/{i}_original.mp3")
#         tfm = sox.Transformer()
#         sample_length = MP3(f"./posts/{post_id}/tts_audio/{i}_original.mp3").info.length
#         print(f"Sample length: {sample_length}")
#         if sample_length > 1.8:
#             tfm.tempo(1.2)
#             tfm.silence(min_silence_duration=0.5)
#         tfm.pad(end_duration=0.5)
#         tfm.build_file(f'./posts/{post_id}/tts_audio/{i}_original.mp3', f'./posts/{post_id}/tts_audio/{i}.mp3')
#         print("Done! Removing intermediary mp3 file...")
#         os.remove(f"./posts/{post_id}/tts_audio/{i}_original.mp3")
#         print(f"Done rendering audio sample #{i}!")