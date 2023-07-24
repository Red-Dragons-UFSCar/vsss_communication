from vss_communication import Referee
import time

ref = Referee(ip='224.5.23.2', port_server=10003, logger=False)

while True:
    ref.update()
    print(ref.get_data())