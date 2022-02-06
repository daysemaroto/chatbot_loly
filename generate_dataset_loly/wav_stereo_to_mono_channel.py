import os

from pydub import AudioSegment
# C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\generate_dataset_loly\wav_stereo
folder_wav_stereo = r'C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\generate_dataset_loly\wav_stereo'

folder_wav_mono = r'C:\Users\josel\Desktop\ESPOL\INTEGRADORA\PROYECTO\TTS_venv\generate_dataset_loly\wav_mono'


for filename in os.listdir(folder_wav_stereo):
  infilename = os.path.join(folder_wav_stereo, filename)
  print(infilename)
  if not os.path.isfile(infilename): continue
  sound = AudioSegment.from_wav(infilename)
  sound = sound.set_channels(1)
  oldbase = os.path.splitext(filename)
  oldbase = oldbase[0]
  file_to_foler_wav = os.path.join(folder_wav_mono, oldbase + '.wav')
  sound.export(file_to_foler_wav, format="wav")
