from bs4 import BeautifulSoup
import requests
from gtts import gTTS
from unidecode import unidecode
import pygame
import os
import time
from mutagen.mp3 import MP3


class Speech():
    def __init__(self):
        pass

    def speak(canto, chapter, sloka):

        pygame.init()

        link = f'https://vedabase.io/en/library/sb/{canto}/{chapter}/{sloka}/'

        response = requests.get(link)

        vedabase_pg = response.text

        soup = BeautifulSoup(vedabase_pg, "html.parser")

        div_element = soup.find(name="div", class_="wrapper-translation")

        translation = unidecode(div_element.getText())
        print(translation)

        tts = gTTS(translation)
        tts.save("example.mp3")
        mp3_file = "example.mp3"

        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()



        audio = MP3(mp3_file)

        # Get the duration in seconds
        duration_sec = audio.info.length

        print(f"The duration of the MP3 file '{mp3_file}' is {duration_sec:.2f} seconds.")

        time.sleep(duration_sec+5)


        pygame.mixer.music.stop()
        pygame.quit()

        if os.path.exists(mp3_file):
            os.remove(mp3_file)
            print(f"The file '{mp3_file}' has been deleted.")
        else:
            print(f"The file '{mp3_file}' does not exist.")