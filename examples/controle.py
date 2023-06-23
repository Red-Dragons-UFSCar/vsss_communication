from vss_communication import StrategyControl

controle = StrategyControl()

while True:
    controle.send_mensage(1, True, 10, 20)
    