# importing libraries
from os.path import exists
from shutil import rmtree
import speech_recognition as sr
import os
from pydub.silence import split_on_silence
from pydub import AudioSegment

folder = r'C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\generate_dataset_loly\wav_mono'

# Setup Directory Data
cwd = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cwd, "dataset")
output_dir_audio = ""
output_dir_audio_temp = ""
output_dir_speech = ""


# Create folders needed for ljspeech
def create_folders():
  global output_dir
  global output_dir_audio
  global output_dir_audio_temp
  global output_dir_speech

  print('→ Creating Dataset Folders')

  output_dir_speech = os.path.join(output_dir, "LJSpeech-1.1")

  # Delete existing folder if exists for clean run
  if os.path.exists(output_dir_speech):
    rmtree(output_dir_speech)

  output_dir_audio = os.path.join(output_dir_speech, "wavs")
  output_dir_audio_temp = os.path.join(output_dir_speech, "temp")

  # Create Clean Folders
  os.makedirs(output_dir_speech)
  os.makedirs(output_dir_audio)
  os.makedirs(output_dir_audio_temp)


# def audio_to_text(file_source):
#   # create a speech recognition object
#   print(file_source)
#   r = sr.Recognizer()
#   with sr.AudioFile(file_source) as source:
#     r.adjust_for_ambient_noise(source)
#     print("Converting Audio File " + file_source + " to Text...")
#     audio = r.record(source)
#     try:
#       text = r.recognize_google(audio, language="es-ES")
#       print("Converted Audio Is: \n" + text)
#       return text
#     except Exception as e:
#       print(e)


# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # create a speech recognition object
    print(path)
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened,  language="es-ES")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text



def create_meta_data(mrs_dir):
  print('→ Creating META Data')

  # Create metadata.csv for ljspeech
  metadata = open(os.path.join(output_dir_speech, "metadata.csv"), mode="w", encoding="utf8")

  # List available recording sessions
  for filename in os.listdir(folder):
    # infilename = os.path.join(folder, filename)
    infilename = os.path.join(folder + os.sep + filename)
    # print(infilename)
    if not os.path.isfile(infilename): continue
    if exists(infilename):
      print(infilename)
      # text = audio_to_text(infilename)
      text = get_large_audio_transcription(infilename)
      text= text.rstrip()
      print('this is the text i get it ======>' + text)
      oldbase = os.path.splitext(filename)
      oldbase = oldbase[0]
      line = str(oldbase) + '|' + str(text) + '|'+ str(text) + '\n'
      metadata.write(line)
      # copyfile(infilename, os.path.join(output_dir_audio_temp, oldbase + ".wav"))
  metadata.close()

def main():
  print('\n\033[48;5;22m  Folder audios to LJ Speech Processor  \033[0m\n')
  create_folders()
  create_meta_data(folder)
  print('\n\033[38;5;86;1m✔\033[0m COMPLETE【ツ】\n')

if __name__ == '__main__':
  main()
