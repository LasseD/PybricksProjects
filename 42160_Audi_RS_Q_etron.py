from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Hardware:
technicHub = TechnicHub()
remote = Remote()
motorFront = Motor(Port.B)
motorRear = Motor(Port.A)
motorSteering = Motor(Port.D)

# State:
speed = 0
steeringTarget = 0
SPEED_ACCELERATE = 5
SPEED_DECELERATE = 2
SPEED_STEERING = 400
MAX_STEERING = -1
STEERING_BOOST = 1.1

def resetSteering():
    global MAX_STEERING
    technicHub.light.on(Color.RED)
    motorSteering.run_until_stalled(SPEED_STEERING)
    maxSteering = motorSteering.angle()
    motorSteering.run_until_stalled(-SPEED_STEERING)
    minSteering = motorSteering.angle()
    MAX_STEERING = (maxSteering-minSteering)/2
    motorSteering.run_target(SPEED_STEERING, (maxSteering+minSteering)/2, then=Stop.HOLD)
    motorSteering.reset_angle()
    technicHub.light.on(Color.GREEN)
    remote.light.on(Color.GREEN)
resetSteering()

while True:
    buttons = remote.buttons.pressed()

    # Acceleration:
    if Button.LEFT in buttons:
        speed = 0
    elif Button.LEFT_PLUS in buttons:
        speed = min(100, speed+SPEED_ACCELERATE)
    elif Button.LEFT_MINUS in buttons:
        speed = max(-100, speed-SPEED_ACCELERATE)
    elif speed > 0:
        speed = max(0, speed - SPEED_DECELERATE)
    else:
        speed = min(0, speed + SPEED_DECELERATE)
    motorFront.dc(speed)
    motorRear.dc(speed)

    # Steering:
    if Button.RIGHT_PLUS in buttons:
        steeringTarget = MAX_STEERING
    elif Button.RIGHT_MINUS in buttons:
        steeringTarget = -MAX_STEERING
    else:
        steeringTarget = 0
    steeringDiff = steeringTarget-motorSteering.angle()
    motorSteering.dc(min(100, max(-100, STEERING_BOOST*steeringDiff)))

    # Turn off using green button:
    if Button.CENTER in buttons:
        technicHub.system.shutdown()

    wait(20)
