from proto import Command
import socket

class StrategyControl():
    def __init__(self, ip = '127.0.0.1', port = 20011, logger=False) -> None:
        #  Protobuff message atributes
        self.robot_id = 0  
        self.yellow_team = 0
        self.wheel_left = 0
        self.wheel_right = 0

        #  Network parameters
        self.ip = ip 
        self.port = port
        self.buffer_size = 1024

        #  Receiver parameters
        self.eletronica_ip = '127.0.0.1' 
        self.eletronica_porta = 20012

        self.create_socket()

        self.logger=logger

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)
    
    def send_mensage(self, index, yellow_team, wheel_left, wheel_right):
        self.robot_id = index
        self.yellow_team = yellow_team
        self.wheel_left = wheel_left
        self.wheel_right = wheel_right

        msg = Command()
        msg.id = self.robot_id
        msg.yellowteam = yellow_team
        msg.wheel_left = self.wheel_left
        msg.wheel_right = self.wheel_right

        try: 
            self.socket.sendto(msg.SerializeToString(), (self.eletronica_ip, self.eletronica_porta))
            if self.logger: print("[S&C] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[S&C] Falha ao enviar. Socket bloqueado")
            else:
                print("[S&C] Socket error:", e)
            

class Actuator():
    def __init__(self, ip='127.0.0.1', port=20012, logger=False):
        #  Protobuff message atributes
        self.robot_id = 0 
        self.yellow_team = 0
        self.wheel_left = 0
        self.wheel_right = 0

        #  Network parameters
        self.ip = ip 
        self.port = port
        self.buffer_size = 1024

        self.create_socket()

        self.logger=logger

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def update(self):
        try: 
            bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            msgRaw = bytesAddressPair[0]
            self.convert_parameters(msgRaw)

            if self.logger:
                print("[ACTUATOR] Recebido!")
            
        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                print("[ACTUATOR] Falha ao receber. Socket bloqueado.")
            else:
                print("[ACTUATOR] Socket error:", e)

    def convert_parameters(self, msgRaw):
        msg = Command()
        msg.ParseFromString(msgRaw)
        
        self.robot_id = msg.id
        self.yellow_team = msg.yellowteam
        self.wheel_left = msg.wheel_left
        self.wheel_right = msg.wheel_right


    
