import shutil
from shutil import rmtree

from pydub import AudioSegment
import os

# Setup Directory Data
cwd = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(cwd, "wav")
output_dir_audio = ""
output_dir_audio_temp = ""
output_dir_speech = ""

folder_mp3 = r'C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\important\dataset_loly\audios\mp3'

folder_wav = r'C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\important\dataset_loly\audios\wav_stereo'


def create_folders():
  global output_dir
  global output_dir_audio
  global output_dir_audio_temp
  global output_dir_speech

  print('→ Creating Dataset Folders')

  output_dir_audio = os.path.join(output_dir_speech, "wav")

  # Delete existing folder if exists for clean run
  if os.path.exists(output_dir_audio):
    rmtree(output_dir_audio)

  # Create Clean Folders
  os.makedirs(output_dir_audio)

def mp3_to_wav():
    for filename in os.listdir(folder_mp3):
        infilename = os.path.join(folder_mp3,filename)
        sound = AudioSegment.from_file(infilename)
        oldbase = os.path.splitext(filename)
        oldbase = oldbase[0]
        newname = infilename.replace('.mp3', '.wav')
        file_to_foler_wav= os.path.join(folder_wav, oldbase + '.wav')
        print(file_to_foler_wav)
        sound.export(file_to_foler_wav, format="wav")

def rename_file_audio_to_LJ_Speech_format():
    count = 1
    for filename in os.listdir(folder_wav):
        infilename = os.path.join(folder_wav,filename)
        print(infilename)
        if not os.path.isfile(infilename): continue
        print(infilename)
        newname_init = 'loly_f' + str(count).zfill(3)
        oldbase = os.path.splitext(filename)
        newname_final = infilename.replace(oldbase[0], newname_init)
        output = os.rename(infilename, newname_final)
        count += 1


def main():
    create_folders()
    mp3_to_wav()
    rename_file_audio_to_LJ_Speech_format()

if __name__ == '__main__':
    main()
