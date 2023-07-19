robot0 = dict([ ("robot_id", 0), ("x", 10), ("y", 20), ("orientation", 1), 
                ("vx", 1.1), ("vy", 0.9), ("vorientation", 0.5) ])
robot1 = dict([ ("robot_id", 1), ("x", 10), ("y", 20), ("orientation", 1), 
                ("vx", 1.1), ("vy", 0.9), ("vorientation", 0.5) ])
robot2 = dict([ ("robot_id", 2), ("x", 10), ("y", 20), ("orientation", 1), 
                ("vx", 1.1), ("vy", 0.9), ("vorientation", 0.5) ])

robots_yellow = [robot0, robot1, robot2]
robots_blue = [robot0, robot1, robot2]

ball = dict([ ("x", 10), ("y", 20), ("z", 0), ("vx", 10), ("vy", 20), ("vz", 0) ])

frame = dict([ ("ball", ball), ("robots_yellow", robots_yellow), ("robots_blue", robots_blue) ])

print(frame["robots_yellow"][1]["robot_id"])


