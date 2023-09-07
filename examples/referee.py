from vss_communication import Referee
import time

ref = Referee()

# Comunicação com a eletronica
dicionario_faltas = dict([ ("foul", 4), ("teamcolor", 0), ("foulQuadrant", 0), 
                           ("timestamp", 0), ("gameHalf", 1) ])
ref.send_mensage(dicionario_faltas) # Envia as informações para a eletrônica
time.sleep(1)
dicionario_faltas = dict([ ("foul", 6), ("teamcolor", 2), ("foulQuadrant", 0), 
                           ("timestamp", 0), ("gameHalf", 1) ])
ref.send_mensage(dicionario_faltas) # Envia as informações para a eletrônica