from vss_communication import StrategyControl

#controle = StrategyControl(ip='224.5.23.2', port=10015, logger=False, pattern='ssl', convert_coordinates=True)  # Criação do objeto do controle e estratégia
controle = StrategyControl(ip='224.0.0.1', port=10002, logger=False, pattern='fira', convert_coordinates=True)

while True:
    # Comunicação com a visão
    controle.update(team_yellow=False)  # Atualiza as informações recebidas da visão
    field = controle.get_data()  # Recebe as informações
    print("Ball y: ", field[0]['ball'])  

    # Comunicação com a eletronica
    #controle.send_mensage(1, True, 10, 20) # Envia as informações para a eletrônica
    