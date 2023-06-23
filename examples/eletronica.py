from vss_communication import Actuator

eletronica = Actuator()

while True:
    eletronica.update()
    print(eletronica.wheel_left)