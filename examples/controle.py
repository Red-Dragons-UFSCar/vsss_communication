from vss_communication import StrategyControl

controle = StrategyControl(logger=False)  # Criação do objeto do controle e estratégia

while True:
    # Comunicação com a visão
    controle.update()  # Atualiza as informações recebidas da visão
    field = controle.get_data()  # Recebe as informações
    print("Ball x: ", field["ball"]["x"])  

    # Comunicação com a eletronica
    controle.send_mensage(1, True, 10, 20) # Envia as informações para a eletrônica
    
