import os
# import librosa
from pydub import AudioSegment as am
folder_wav_mono = r'C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\generate_dataset_loly\wav_mono'


for filename in os.listdir(folder_wav_mono):
  infilename = os.path.join(folder_wav_mono, filename)
  print(infilename)
  if not os.path.isfile(infilename): continue
  # to resample at 4800KHz, to 44.1khz
  # librosa.load(infilename, sr=44100)
  sound = am.from_file(infilename, format='wav', frame_rate=48000)
  sound = sound.set_frame_rate(22050)
  oldbase = os.path.splitext(filename)
  oldbase = oldbase[0]
  file_to_foler_wav = os.path.join(folder_wav_mono, oldbase + '.wav')
  sound.export(file_to_foler_wav, format='wav')
