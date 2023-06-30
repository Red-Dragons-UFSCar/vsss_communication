from vss_communication import Actuator

eletronica = Actuator()

while True:
    eletronica.update()
    data = eletronica.get_data()
    print("Indicie: ", data["robot_id"])
    print("Time: ", data["yellow_team"])
    print("Velocidade Esquerda: ", data["wheel_left"])
    print("Velocidade Direita: ", data["wheel_right"])