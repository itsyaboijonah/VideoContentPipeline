# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import gtts
from playsound import playsound

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = ["this is a test", "multiple strings rendered here", "just gotta scrape them", "and make the videos"]

    for i in range(len(test)):
        tts = gtts.gTTS(test[i], lang="en-uk")
        tts.save(f"hello{i}.mp3")
        playsound(f"hello{i}.mp3")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
