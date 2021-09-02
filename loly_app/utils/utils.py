#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import calendar
import os
import time
import contextlib
import wave


def loly_tts(sentence, synthesizer, out_path='loly-audios/',):
    nueva_data = {}
    texto = sentence
    print(synthesizer.vocoder_model)
    wav = synthesizer.tts(texto, None, None)
    ts=calendar.timegm(time.gmtime())
    save_path = os.path.join(out_path, str(ts) + '.wav')
    synthesizer.save_wav(wav, save_path)
    fname = save_path
    with contextlib.closing(wave.open(fname, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    new_dict = {'archivo': save_path, 'texto': texto, 'duracion': str(duration), 'ubicacion': 'audios/'+str(ts) + '.wav'}
    nueva_data[str(ts)] = new_dict
    resultado = new_dict
    return resultado