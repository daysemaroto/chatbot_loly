#!/bin/sh
source /Users/adriantomala/Desktop/TTS-main/venv/bin/activate; 
python3 /Users/adriantomala/Desktop/TTS-main/TTS/bin/loly/synthesize_loly.py --config_path /Users/adriantomala/Desktop/TTS-main/TTS/bin/loly/config.json --model_path /Users/adriantomala/Desktop/TTS-main/TTS/bin/loly/maldy.pth.tar  --out_path /Users/adriantomala/Desktop/TTS-main/TTS/bin/loly/audios --json_path /Users/adriantomala/Desktop/TTS-main/TTS/bin/loly/json; 
deactivate;