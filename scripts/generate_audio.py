from scripts.post_parser import Post, Comment, Reply
from scripts.scraper import load_from_pickle
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os, sys, random, paths

session = Session(profile_name='polly_tts_user')
polly = session.client('polly', region_name='us-east-2')
polly_voices = ['Nicole', 'Russell', 'Amy', 'Emma', 'Brian', 'Aditi', 'Raveena', 'Joanna', 'Kendra', 'Kimberly', 'Salli', 'Joey', 'Matthew', 'Geraint']


def render(text_to_render, tts_voice_name, output_filename):
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text_to_render, OutputFormat="mp3",
                                           VoiceId=tts_voice_name)
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


def generate_audio(batch_name, post_id):
    post = load_from_pickle(f"{paths.batch_scrapes_path}{batch_name}/parsed/{post_id}.pkl")
    author_voices = {}
    post_authors = post.get_authors()
    for author in post_authors:
        if author not in author_voices:
            author_voices[author] = random.choice(polly_voices)

    os.makedirs(f"{paths.posts_path}{post_id}/tts_audio", exist_ok=True)
    for i, (author, content) in enumerate(post.flatten()):
        print(f"Processing audio sample #{i}...")
        print(f"Author: {author}\n"
              f"Content: {content}")
        render(content, author_voices[author], f"{paths.posts_path}{post_id}/tts_audio/{i}.mp3")
        print(f"Done rendering audio sample #{i}!")
