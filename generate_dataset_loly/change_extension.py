import os
import sys
folder = 'C:/Users/josel/Desktop/ESPOL/INTEGRADORA/PROYECTO/TTS_venv/important/dataset_loly/audios/mp3'
for filename in os.listdir(folder):
    infilename = os.path.join(folder,filename)
    if not os.path.isfile(infilename): continue
    print(infilename)
    oldbase = os.path.splitext(filename)
    newname = infilename.replace('.mp3', '.wav')
    output = os.rename(infilename, newname)


