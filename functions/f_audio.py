import gtts
from playsound import playsound
#from langdetect import detect

import os

#passa os parametros para o audia
def audiodescricao(resp):
   
   fala = gtts.gTTS(resp, lang="pt")
#salva o audio
   
   caminho = os.path.dirname(__file__) + 'audio.mp3'
   fala.save(caminho)
#executa o audio

   playsound(caminho)
   # os.remove(caminho)