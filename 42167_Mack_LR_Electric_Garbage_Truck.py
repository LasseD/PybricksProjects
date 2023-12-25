from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait, StopWatch

remote = Remote()
arm = Motor(Port.B)
steer = Motor(Port.D)
drive = Motor(Port.F)
ACCELERATION = 1.8
SPEED_ARM = 150
STEERING_BOOST = 1.7
greenButtonHoldTime = StopWatch()
greenButtonDown = False
TIME_TURN_OFF = 2000
speed = 0

def runArm():
    remote.light.on(Color.RED)
    arm.run_target(SPEED_ARM, -70)
    arm.run_target(2*SPEED_ARM, -60)
    arm.run_target(2*SPEED_ARM, -70)
    arm.run_target(2*SPEED_ARM, -60)
    arm.run_target(2*SPEED_ARM, -70)
    arm.run_target(SPEED_ARM, 120)
    remote.light.on(Color.GREEN)

# Reset:
arm.run_target(SPEED_ARM, 120)
steer.run_until_stalled(400)
MAX_STEERING = steer.angle()
print("Left steering max", MAX_STEERING)
steer.run_until_stalled(-400)
MIN_STEERING = steer.angle()
print("Right steering max", -MIN_STEERING)

while True:
    buttons = remote.buttons.pressed()

    # Acceleration:
    if Button.LEFT in buttons:
        speed = 0
    elif Button.LEFT_PLUS in buttons:
        speed = min(100, speed+2*ACCELERATION)
    elif Button.LEFT_MINUS in buttons:
        speed = max(-100, speed-ACCELERATION)
    elif speed > 0:
        speed = max(0, speed - ACCELERATION)
    else:
        speed = min(0, speed + ACCELERATION)
    drive.dc(speed)

    # Steering:
    if Button.RIGHT_PLUS in buttons:
        steeringTarget = MIN_STEERING
    elif Button.RIGHT_MINUS in buttons:
        steeringTarget = MAX_STEERING
    else:
        steeringTarget = 0
    steeringDiff = steeringTarget-steer.angle()
    steer.dc(min(100, max(-100, STEERING_BOOST*steeringDiff)))

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
                runArm()
        greenButtonDown = False

    wait(20)
