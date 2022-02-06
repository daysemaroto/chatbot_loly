# Pasos para crear el dataset para entrenar el modelo de sintesis de voz

Si tiene audios en formato .wav saltarse al paso 2

1. Crear una carpeta llamada mp3
2. Crear una carpeta llamada wav_stereo
3. Crear una carpeta llamada wav_mono

4. Coloque todos sus audios en formato .mp3 en su carpeta mp3

5. Convertir archivos de audio de .mp3 to .wav con el siguiente script
```
python ./mp3_to_wav.py
```

6. Pasar los audios en formato .wav que son channel stereo to channel mono con el siguiente script

```
python ./wav_stereo_to_mono_channel.py
```

7. Cambiar el sample rate de los audios con channel mono to sample-rate 25050
```
python ./set_simple_rate_to_25050.py
```


5. Generar el dataset de texto con el siguiente script

```
python ./audio_to_LJ_SpeechFormat_dataset.py
```
El texto se generará en la siguiente ruta:

***.\dataset\LJSpeech-1.1***