import os

from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
from utils.utils import loly_tts

from TTS.utils.synthesizer import Synthesizer

synthesizer = Synthesizer(
    tts_checkpoint=os.path.join(settings.BASE_DIR, 'config/maldy.pth.tar'),
    tts_config_path=os.path.join(settings.BASE_DIR, 'config/config.json'),
    #vocoder_config=os.path.join(settings.BASE_DIR, 'config/vocoder/config_vocoder.json'),
    #vocoder_checkpoint=os.path.join(settings.BASE_DIR, 'config/vocoder/vocoder_model.pth.tar'),
    use_cuda=False,
    )
def index(request):
    return render(request, 'index.html')

def generar_voz(request):
    if request.method == 'POST':
        #Obtener Data del POST
        sentence = ','+request.POST.get('dialogo')+','

        resultado = loly_tts(sentence=sentence,  synthesizer=synthesizer, out_path=os.path.join(settings.BASE_DIR, 'static/audios'))
        #Ejecuta Shell Script para generar el audio
        #Ejemplo: '/Users/adriantomala/Desktop/voice_script_single.sh "Este es el dialogo" "1"'
        #process = subprocess.Popen('/Users/adriantomala/Desktop/voice_script_single.sh "'+sentence+'" "'+str(id_evento)+'"', shell=True, stdout=subprocess.PIPE)

        #Espera que el script termine de ejecutarse
        #process.wait()

        #Obtiene la duracion del audio generado
        #process.stdout.readlines() obtiene todas las lineas que imprime el script en python en una lista
        #al obtener el ultimo index, obtenemos lo ultimo que imprime que es la duracion del audio en bytes
        #decode("utf-8") convierte de bytes a string
        #duracion = (process.stdout.readlines()[-1]).decode("utf-8")

        #Obtiene la ubicacion del audio generado
        #ubicacion = "audios/"+str(id_evento)+".wav"

        return render(request, 'response.html', {'dialogo': sentence, 'resultado': resultado})
    else:
        return redirect('/')