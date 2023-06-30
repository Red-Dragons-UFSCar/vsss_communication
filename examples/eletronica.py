from vss_communication import Actuator

eletronica = Actuator()

while True:
    eletronica.update()
    print("Indicie: ", eletronica.robot_id)
    print("Time: ", eletronica.yellow_team)
    print("Velocidade Esquerda: ", eletronica.wheel_left)
    print("Velocidade Direita: ", eletronica.wheel_right)