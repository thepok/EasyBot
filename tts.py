from gtts import gTTS
import os
from datetime import datetime

class AudioGenerator:
    def __init__(self):
        pass

    def GenerateAudioAtomic(self, text, lang="en"):
        tts = gTTS(text=text, lang=lang)
        tts.save("audio.mp3")
        with open("audio.mp3", "rb") as f:
            audio = f.read()
        os.remove("audio.mp3")
        return audio

    def generate_audio(self, text, lang="en"):
        splits = self.split_sentences(text, 1000)
        audio = b''
        total_splits = len(splits)
        for i, split in enumerate(splits, 1):
            audio += self.GenerateAudioAtomic(" " + split + " ", lang=lang)
            print(f"Progress: {i}/{total_splits} splits processed")  # Progress info
        return audio

    def split_sentences(self, text, maxLength):
        import re
        sentences = re.split('(?<=[.!?]) +', text)
        output = []
        current_string = ''
        for sentence in sentences:
            if len(current_string) + len(sentence) + 1 > maxLength:
                output.append(current_string.strip())
                current_string = ''
            current_string += sentence + ' '
        if current_string:
            output.append(current_string.strip())
        return output

    def generate_and_save_audio(self, text, lang="en", filename=None, folder_path=None):
        audio = self.generate_audio(text, lang)
        
        if filename is None:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio-{current_time}.mp3"
        
        if folder_path:
            os.makedirs(folder_path, exist_ok=True)
            full_path = os.path.join(folder_path, filename)
        else:
            full_path = filename

        with open(full_path, "wb") as f:
            f.write(audio)

        print(f"Audio saved to: {full_path}")
        return full_path


    def say(self, text, lang="en"):
        import pygame
        audio_path = self.generate_and_save_audio(text, lang=lang)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
        os.remove(audio_path)

if __name__ == "__main__":
    audio_generator = AudioGenerator()

    text =" ... Hallo ich bin ein [englisch] bot!"

    audio_generator.say(text, lang="de")