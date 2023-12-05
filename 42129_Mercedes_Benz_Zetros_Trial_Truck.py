from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, DCMotor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

# Hardware:
technicHub = TechnicHub()
motorGear = DCMotor(Port.C)
motorRear1 = Motor(Port.A)
motorRear2 = Motor(Port.B)
motorSteering = Motor(Port.D)

# State:
speed = 0
steeringTarget = 0
SPEED_ACCELERATE = 5
SPEED_DECELERATE = 2
SPEED_STEERING = 600
MAX_STEERING = -1
MIN_STEERING_POWER = 20
MAX_STEERING_POWER = 100
STEERING_BOOST = 4.0
# Green button used to change gears and turn off:
greenButtonHoldTime = StopWatch()
greenButtonDown = False
TIME_TURN_OFF = 2000

def reset():
    motorGear.dc(100)
    global MAX_STEERING
    technicHub.light.on(Color.RED)
    motorSteering.run_until_stalled(SPEED_STEERING)
    maxSteering = motorSteering.angle()
    motorSteering.run_until_stalled(-SPEED_STEERING)
    minSteering = motorSteering.angle()
    MAX_STEERING = (maxSteering-minSteering)/2
    motorSteering.run_target(SPEED_STEERING, (maxSteering+minSteering)/2, then=Stop.HOLD)
    motorSteering.reset_angle(0)
    technicHub.light.on(Color.GREEN)
    motorGear.stop()
reset()

remote = Remote() # Connect remote. Halts until successful connection

gearLocked = False
remote.light.on(Color.GREEN)
technicHub.light.on(Color.GREEN)
def changeGears():
    global gearLocked
    motorGear.dc(100 if gearLocked else -100)
    wait(2000)
    motorGear.stop()
    gearLocked = not gearLocked
    remote.light.on(Color.RED if gearLocked else Color.GREEN)
    technicHub.light.on(Color.RED if gearLocked else Color.GREEN)

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
    motorRear1.dc(speed)
    motorRear2.dc(speed)

    # Steering:
    if Button.RIGHT_PLUS in buttons:
        steeringTarget = steeringTarget + MAX_STEERING/15
    elif Button.RIGHT_MINUS in buttons:
        steeringTarget = steeringTarget - MAX_STEERING/15
    elif Button.RIGHT in buttons:
        steeringTarget = 0
    # Ensure steering target is within range:
    steeringTarget = max(-MAX_STEERING, min(MAX_STEERING, steeringTarget))
    steeringDiff = steeringTarget-motorSteering.angle()
    steeringDC = min(MAX_STEERING_POWER, max(-MAX_STEERING_POWER, STEERING_BOOST*steeringDiff))
    if abs(steeringDC) > MIN_STEERING_POWER:
        motorSteering.dc(steeringDC)
    else:
        motorSteering.dc(0)

    # Turn off using green button:
    if Button.CENTER in buttons:
        if not greenButtonDown:
            greenButtonHoldTime.reset()
        greenButtonDown = True
    else:
        if greenButtonDown:
            if greenButtonHoldTime.time() > TIME_TURN_OFF:
                technicHub.system.shutdown()
            else:
                changeGears()
        greenButtonDown = False

    wait(20)

