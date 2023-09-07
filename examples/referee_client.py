from vss_communication import Referee
import time

ref = Referee(logger=False)

while True:
    ref.update()
    print(ref.get_data())
