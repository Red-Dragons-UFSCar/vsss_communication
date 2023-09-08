from proto import Command, Environment, VSSRef_Command, SSL_WrapperPacket
import socket
import struct
import time

class StrategyControl():
    def __init__(self, ip = '127.0.0.1', port = 20011, actuator_ip = '127.0.0.1', 
                 actuator_port = 20012, yellowTeam=False, logger=False, pattern='fira', 
                 convert_coordinates = True) -> None:
        #  Network parameters
        self.ip = ip 
        self.port = port
        self.buffer_size = 1024

        #  Receiver parameters
        self.actuator_ip = actuator_ip
        self.actuator_port = actuator_port

        self.yellow_team = yellowTeam

        # Logger control
        self.logger=logger

        self.pattern = pattern
        self.convert_coordinates = convert_coordinates

        self.create_socket()
        self.start_frame()

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 128)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack("=4sl", socket.inet_aton(self.ip), socket.INADDR_ANY))
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def start_frame(self):
        robots_blue = []
        robots_yellow = []
        for i in range(0, 3):
            robots_blue.append( dict([ ("robot_id", 0), 
                                       ("x", 0), 
                                       ("y", 0), 
                                       ("orientation", 0), 
                                       ("vx", 0), 
                                       ("vy", 0), 
                                       ("vorientation", 0) ]) )
            robots_yellow.append( dict([ ("robot_id", 0), 
                                       ("x", 0), 
                                       ("y", 0), 
                                       ("orientation", 0), 
                                       ("vx", 0), 
                                       ("vy", 0), 
                                       ("vorientation", 0) ]) )
        ball = dict([ ("x", 0), 
                        ("y", 0), 
                        ("z", 0), 
                        ("vx", 0), 
                        ("vy", 0), 
                        ("vz", 0) ])

        self.frame = dict([ ("ball", ball), 
                            ("robots_yellow", robots_yellow), 
                            ("robots_blue", robots_blue), 
                            ("our_bots", robots_blue), 
                            ("their_bots", robots_yellow) ])


    
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
            self.socket.sendto(msg.SerializeToString(), (self.actuator_ip, self.actuator_port))
            if self.logger: print("[S&C] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[S&C] Falha ao enviar. Socket bloqueado")
            else:
                print("[S&C] Socket error:", e)
    
    def convert_parameters(self, msgRaw, team_yellow):
        msg = Environment()
        msg.ParseFromString(msgRaw)
        msg_robots_blue = msg.frame.robots_blue
        msg_robots_yellow = msg.frame.robots_yellow
        msg_ball = msg.frame.ball

        geometry_field_length = 1.5
        geometry_field_width = 1.3
        geometry_goal_depth = 0.1

        if self.convert_coordinates:
            correction_position_x = geometry_field_length/2 + geometry_goal_depth
            correction_position_y = geometry_field_width/2
            for i in range(0, len(msg_robots_blue)):
                msg_robots_blue[i].x = (msg_robots_blue[i].x + correction_position_x)*100
                msg_robots_blue[i].y = (msg_robots_blue[i].y + correction_position_y)*100
            for i in range(0, len(msg_robots_yellow)):
                msg_robots_yellow[i].x = (msg_robots_yellow[i].x + correction_position_x)*100
                msg_robots_yellow[i].y = (msg_robots_yellow[i].y + correction_position_y)*100
            msg.frame.ball.x = (msg.frame.ball.x + correction_position_x)*100
            msg.frame.ball.y = (msg.frame.ball.y + correction_position_y)*100

        robots_blue = []
        robots_yellow = []
        for i in range(0, len(msg_robots_blue)):
            robots_blue.append( dict([ ("robot_id", msg_robots_blue[i].robot_id), 
                                       ("x", msg_robots_blue[i].x), 
                                       ("y", msg_robots_blue[i].y), 
                                       ("orientation", msg_robots_blue[i].orientation), 
                                       ("vx", msg_robots_blue[i].vx), 
                                       ("vy", msg_robots_blue[i].vy), 
                                       ("vorientation", msg_robots_blue[i].vorientation) ]) )
        for i in range(0, len(msg_robots_yellow)):
            robots_yellow.append( dict([ ("robot_id", msg_robots_yellow[i].robot_id), 
                                       ("x", msg_robots_yellow[i].x), 
                                       ("y", msg_robots_yellow[i].y), 
                                       ("orientation", msg_robots_yellow[i].orientation), 
                                       ("vx", msg_robots_yellow[i].vx), 
                                       ("vy", msg_robots_yellow[i].vy), 
                                       ("vorientation", msg_robots_yellow[i].vorientation) ]) )
        ball = dict([ ("x", msg.frame.ball.x), 
                        ("y", msg.frame.ball.y), 
                        ("z", msg.frame.ball.z), 
                        ("vx", msg.frame.ball.vx), 
                        ("vy", msg.frame.ball.vy), 
                        ("vz", msg.frame.ball.vz) ])


        if team_yellow:
            self.frame = dict([ ("ball", ball), 
                                ("robots_yellow", robots_yellow), 
                                ("robots_blue", robots_blue), 
                                ("our_bots", robots_yellow), 
                                ("their_bots", robots_blue)])
        else:
            self.frame = dict([ ("ball", ball), 
                                ("robots_yellow", robots_yellow), 
                                ("robots_blue", robots_blue), 
                                ("our_bots", robots_blue), 
                                ("their_bots", robots_yellow)])
            
    def convert_parameters_ssl(self, msgRaw, team_yellow):
        msg = SSL_WrapperPacket()
        msg.ParseFromString(msgRaw)

        msg_robots_blue = msg.detection.robots_blue
        msg_robots_yellow = msg.detection.robots_yellow
        msg_ball = msg.detection.balls
        msg_geometry = msg.geometry

        if self.convert_coordinates:
            correction_position_x = msg_geometry.field.field_length/2 + msg_geometry.field.goal_depth
            correction_position_y = msg_geometry.field.field_width/2
            for i in range(0, len(msg_robots_blue)):
                msg_robots_blue[i].x = (msg_robots_blue[i].x + correction_position_x)/10
                msg_robots_blue[i].y = (msg_robots_blue[i].y + correction_position_y)/10
            for i in range(0, len(msg_robots_yellow)):
                msg_robots_yellow[i].x = (msg_robots_yellow[i].x + correction_position_x)/10
                msg_robots_yellow[i].y = (msg_robots_yellow[i].y + correction_position_y)/10
            msg_ball[0].x = (msg_ball[0].x + correction_position_x)/10
            msg_ball[0].y = (msg_ball[0].y + correction_position_y)/10

        robots_blue = []
        robots_yellow = []
        for i in range(0, len(msg_robots_blue)):
            robots_blue.append( dict([ ("robot_id", msg_robots_blue[i].robot_id), 
                                       ("x", msg_robots_blue[i].x), 
                                       ("y", msg_robots_blue[i].y), 
                                       ("orientation", msg_robots_blue[i].orientation), 
                                       ("vx", 0), 
                                       ("vy", 0), 
                                       ("vorientation", 0) ]) )
        for i in range(0, len(msg_robots_yellow)):
            robots_yellow.append( dict([ ("robot_id", msg_robots_yellow[i].robot_id), 
                                       ("x", msg_robots_yellow[i].x), 
                                       ("y", msg_robots_yellow[i].y), 
                                       ("orientation", msg_robots_yellow[i].orientation), 
                                       ("vx", 0), 
                                       ("vy", 0), 
                                       ("vorientation", 0)]) )
        ball = dict([ ("x", msg_ball[0].x), 
                        ("y", msg_ball[0].y), 
                        ("z", msg_ball[0].z), 
                        ("vx", 0), 
                        ("vy", 0), 
                        ("vz", 0) ])
        
        if team_yellow:
            self.frame = dict([ ("ball", ball), 
                                ("robots_yellow", robots_yellow), 
                                ("robots_blue", robots_blue), 
                                ("our_bots", robots_yellow), 
                                ("their_bots", robots_blue)])
        else:
            self.frame = dict([ ("ball", ball), 
                                ("robots_yellow", robots_yellow), 
                                ("robots_blue", robots_blue), 
                                ("our_bots", robots_blue), 
                                ("their_bots", robots_yellow)])
    
    def update(self, team_yellow):
        msgRaw = None
        try: 
            bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            msgRaw = bytesAddressPair[0]
            if self.pattern == 'fira':
                self.convert_parameters(msgRaw, team_yellow)
            elif self.pattern == 'ssl':
                self.convert_parameters_ssl(msgRaw, team_yellow)
            else:
                print("[S&C] ERRO: Padrão não reconhecido")
            self.error = 0

            if self.logger:
                print("[S&C] Recebido!")
            
        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                self.error = 1
                if self.logger:
                    print("[S&C] Falha ao receber. Socket bloqueado.")
            else:
                self.error = 2
                print("[S&C] Socket error:", e)

    def get_data(self):
        return self.frame, self.error
    
    def get_data_Red(self):
        return dict([("ball", self.frame["ball"]), 
                    ("our_bots", self.frame["robots_blue"]), 
                    ("their_bots", self.frame["robots_yellow"])]), self.error
            

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

        self.error = 1

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def convert_parameters(self, msgRaw):
        msg = Command()
        msg.ParseFromString(msgRaw)
        
        self.robot_id = msg.id
        self.yellow_team = msg.yellowteam
        self.wheel_left = msg.wheel_left
        self.wheel_right = msg.wheel_right

    def update(self):
        try: 
            bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            msgRaw = bytesAddressPair[0]
            self.convert_parameters(msgRaw)
            self.error = 0

            if self.logger:
                print("[ACTUATOR] Recebido!")
            
        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                self.error = 1
                if self.logger:
                    print("[ACTUATOR] Falha ao receber. Socket bloqueado.")
            else:
                print("[ACTUATOR] Socket error:", e)
                self.error = 2

    def get_data(self):
        data = dict([ ("robot_id", self.robot_id), ("yellow_team", self.yellow_team),
                      ("wheel_left", self.wheel_left), ("wheel_right", self.wheel_right) ])
        return data, self.error


class Vision():
    def __init__(self, ip='127.0.0.1', port=20013, logger=True):
        #  Protobuff message atributes
        self.robot_id = 0 
        self.yellow_team = 0
        self.wheel_left = 0
        self.wheel_right = 0

        #  Network parameters
        self.ip = ip 
        self.port = port
        self.buffer_size = 1024

        self.strategy_ip = '127.0.0.1'
        self.strategy_port = 20020

        self.create_socket()

        self.logger=logger

    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def send_mensage(self, frame):
        msg = Environment()

        robot_blue_0 = msg.frame.robots_blue.add()
        robot_blue_1 = msg.frame.robots_blue.add()
        robot_blue_2 = msg.frame.robots_blue.add()
        
        robots_blue = [robot_blue_0, robot_blue_1, robot_blue_2]

        robot_yellow_0 = msg.frame.robots_yellow.add()
        robot_yellow_1 = msg.frame.robots_yellow.add()
        robot_yellow_2 = msg.frame.robots_yellow.add()
        
        robots_yellow = [robot_yellow_0, robot_yellow_1, robot_yellow_2]

        for i in range(0, len(robots_blue)):
            robots_blue[i].robot_id = frame["robots_blue"][i]["robot_id"]
            robots_blue[i].x = frame["robots_blue"][i]["x"]
            robots_blue[i].y = frame["robots_blue"][i]["y"]
            robots_blue[i].orientation = frame["robots_blue"][i]["orientation"]
            robots_blue[i].vx = frame["robots_blue"][i]["vx"]
            robots_blue[i].vy = frame["robots_blue"][i]["vy"]
            robots_blue[i].vorientation = frame["robots_blue"][i]["vorientation"]

            robots_yellow[i].robot_id = frame["robots_yellow"][i]["robot_id"]
            robots_yellow[i].x = frame["robots_yellow"][i]["x"]
            robots_yellow[i].y = frame["robots_yellow"][i]["y"]
            robots_yellow[i].orientation = frame["robots_yellow"][i]["orientation"]
            robots_yellow[i].vx = frame["robots_yellow"][i]["vx"]
            robots_yellow[i].vy = frame["robots_yellow"][i]["vy"]
            robots_yellow[i].vorientation = frame["robots_yellow"][i]["vorientation"]
        
        msg.frame.ball.x = frame["ball"]["x"]
        msg.frame.ball.y = frame["ball"]["y"]
        msg.frame.ball.z = frame["ball"]["z"]
        msg.frame.ball.vx = frame["ball"]["vx"]
        msg.frame.ball.vy = frame["ball"]["vy"]
        msg.frame.ball.vz = frame["ball"]["vz"]

        try: 
            self.socket.sendto(msg.SerializeToString(), (self.strategy_ip, self.strategy_port))
            if self.logger: print("[Vision] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[Vision] Falha ao enviar. Socket bloqueado")
            else:
                print("[Vision] Socket error:", e)

class Referee():
    def __init__(self, ip='127.0.0.1', port=20014, logger=True) -> None:
        self.ip = ip
        self.port = port
        self.buffer_size = 1024

        self.create_socket()

        self.logger = logger
        
        self.foul = 0
        self.teamcolor = 0
        self.foulQuadrant = 0
        self.timestamp = 0
        self.gameHalf = 0

        self.error = 0
    
    def create_socket(self):
        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.setblocking(False) 
        self.socket.settimeout(0.0)

    def send_mensage(self, fouls):
        msg = VSSRef_Command()

        msg.foul = fouls["foul"]
        msg.teamcolor = fouls["teamcolor"]
        msg.foulQuadrant = fouls["foulQuadrant"]
        msg.timestamp = fouls["timestamp"]
        msg.gameHalf = fouls["gameHalf"]

        try: 
            self.socket.sendto(msg.SerializeToString(), (self.ip, self.port))
            if self.logger: print("[REFEREE] Enviado!")

        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                if self.logger:
                    print("[REFEREE] Falha ao enviar. Socket bloqueado")
            else:
                print("[REFEREE] Socket error:", e)

    def update(self):
        try: 
            bytesAddressPair = self.socket.recvfrom(self.buffer_size)
            msgRaw = bytesAddressPair[0]
            self.convert_parameters(msgRaw)
            self.error = 0

            if self.logger:
                print("[REFEREE] Recebido!")
            
        except socket.error as e:
            if e.errno == socket.errno.EAGAIN:
                self.error = 1
                if self.logger:
                    print("[REFEREE] Falha ao receber. Socket bloqueado.")
            else:
                print("[REFEREE] Socket error:", e)
                self.error = 2

    def convert_parameters(self, msgRaw):
        msg = VSSRef_Command()
        msg.ParseFromString(msgRaw)
        
        self.foul = msg.foul
        self.teamcolor = msg.teamcolor
        self.foulQuadrant = msg.foulQuadrant
        self.timestamp = msg.timestamp
        self.gameHalf = msg.gameHalf

    def get_data(self):
        data = dict([("foul", self.foul), ("teamcolor", self.teamcolor), 
                     ("foulQuadrant", self.foulQuadrant), ("timestamp", self.timestamp), 
                     ("gameHalf", self.gameHalf)])
        return data, self.error

    def close_socket(self):
        print("[REFEREE] Socket fechado.")
        self.socket.close()