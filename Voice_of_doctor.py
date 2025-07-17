# # if you dont use pipenv uncomment the following:
# # from dotenv import load_dotenv
# # load_dotenv()

# #Step1a: Setup Text to Speech–TTS–model with gTTS
# import os
from gtts import gTTS

# def text_to_speech_with_gtts_old(input_text, output_filepath):
#     language="en"

#     audioobj= gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)


# input_text="Hi this is Ai with Hassan!"
# # text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

# #Step1b: Setup Text to Speech–TTS–model with ElevenLabs
# # import elevenlabs
# # from elevenlabs.client import ElevenLabs

# # ELEVENLABS_API_KEY=os.environ.get("ELEVEN_API_KEY")

# # def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
# #     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
# #     audio=client.generate(
# #         text= input_text,
# #         voice= "Aria",
# #         output_format= "mp3_22050_32",
# #         model= "eleven_turbo_v2"
# #     )
# #     elevenlabs.save(audio, output_filepath)

# #text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

# #Step2: Use Model for Text output to Voice

# import subprocess
# import platform

# def text_to_speech_with_gtts(input_text, output_filepath):
#     language="en"

#     audioobj= gTTS(
#         text=input_text,
#         lang=language,
#         slow=False
#     )
#     audioobj.save(output_filepath)
#     os_name = platform.system()
#     try:
#         if os_name == "Darwin":  # macOS
#             subprocess.run(['afplay', output_filepath])
#         elif os_name == "Windows":  # Windows
#             subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
#         elif os_name == "Linux":  # Linux
#             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
#         else:
#             raise OSError("Unsupported operating system")
#     except Exception as e:
#         print(f"An error occurred while trying to play the audio: {e}")


# input_text="Hi this is Ai with Hassan, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


# # def text_to_speech_with_elevenlabs(input_text, output_filepath):
# #     client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
# #     audio=client.generate(
# #         text= input_text,
# #         voice= "Aria",
# #         output_format= "mp3_22050_32",
# #         model= "eleven_turbo_v2"
# #     )
# #     elevenlabs.save(audio, output_filepath)
# #     os_name = platform.system()
# #     try:
# #         if os_name == "Darwin":  # macOS
# #             subprocess.run(['afplay', output_filepath])
# #         elif os_name == "Windows":  # Windows
# #             subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
# #         elif os_name == "Linux":  # Linux
# #             subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
# #         else:
# #             raise OSError("Unsupported operating system")
# #     except Exception as e:
# #         print(f"An error occurred while trying to play the audio: {e}")

# #text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3")

import os
from pydub import AudioSegment
import tempfile
import subprocess
import platform
import time

# Explicitly set the path to ffmpeg executable if it's not found automatically
# ONLY UNCOMMENT AND SET THIS if `ffmpeg -version` in a new terminal doesn't work
# and you've verified your PATH. Replace with your actual path.
# os.environ["FFMPEG_PATH"] = r"C:\path\to\your\ffmpeg\bin\ffmpeg.exe"
# os.environ["FFPROBE_PATH"] = r"C:\path\to\your\ffmpeg\bin\ffprobe.exe"


def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows
            temp_wav_filepath = None
            try:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
                    temp_wav_filepath = temp_wav_file.name

                audio = AudioSegment.from_mp3(output_filepath)
                audio.export(temp_wav_filepath, format="wav")

                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{temp_wav_filepath}").PlaySync();'], check=True)
                print(f"Played '{output_filepath}' (via temporary WAV) successfully.")

            except FileNotFoundError:
                print("Error: ffmpeg or libav is not installed or not found in PATH. "
                      "Cannot convert MP3 to WAV for playback on Windows. "
                      "Please install ffmpeg (https://ffmpeg.org/download.html) "
                      "and ensure it's in your system PATH, or set os.environ['FFMPEG_PATH'] explicitly.")
            except Exception as e:
                print(f"An error occurred during WAV conversion or playback on Windows: {e}")
            finally:
                if temp_wav_filepath and os.path.exists(temp_wav_filepath):
                    os.remove(temp_wav_filepath)
                    print(f"Removed temporary WAV file: {temp_wav_filepath}")
        elif os_name == "Linux":  # Linux
            try:
                subprocess.run(['mpg123', output_filepath], check=True)
            except FileNotFoundError:
                print("Warning: mpg123 not found. Trying aplay (might not work for MP3).")
                subprocess.run(['aplay', output_filepath], check=True)
            except Exception as e:
                print(f"An error occurred while trying to play the audio on Linux: {e}")
        else:
            raise OSError(f"Unsupported operating system: {os_name}")
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode} and output:\n{e.stderr.decode()}")
    except Exception as e:
        print(f"An unexpected error occurred while trying to play the audio: {e}")

input_text="Hi this is Ai with Hassan, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")