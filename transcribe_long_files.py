import os
import openai
from pydub import AudioSegment
from dotenv import load_dotenv

# convert m4a to wav
# ffmpeg -i audio1837788862.m4a -acodec pcm_s16le -ac 1 -ar 16000 audio1837788862.wav


def config():
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_KEY')


def audio_to_text(filename):
    audio = AudioSegment.from_mp3(filename)
    ten_minutes = 10 * 60 * 1000
    transcript = []
    for i in range(0, len(audio), ten_minutes):
        first_10_minutes = audio[i:i + ten_minutes]
        first_10_minutes.export("C:/Users/rudae/Downloads/audio.mp3", format="mp3")
        audio_file = open("C:/Users/rudae/Downloads/audio.mp3", "rb")
        result = openai.Audio.translate("whisper-1", audio_file)
        transcript.append(result["text"])
    return transcript


def main():
    """
    The main function that is called when the script is run.
    :return: None
    """
    config()
    transcript = audio_to_text("C:/Users/rudae/Downloads/Lex_Fridman_Podcast.mp3")
    with open("C:/Users/rudae/Downloads/Lex_Fridman_Podcast.txt", "w") as f:
        f.write(" ".join(transcript))


if __name__ == "__main__":
    main()
