from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Port, Color
from pybricks.tools import wait, StopWatch

hub = PrimeHub()
hub.light.off()
hub.display.off() # No circular lights on this model.
remote = Remote()
arm = Motor(Port.B)
steer = Motor(Port.D)
drive = Motor(Port.F)
ACCELERATION = 1.8
SPEED_ARM = 190
STEERING_BOOST = 1.7
MIN_DC = 20
TIME_TURN_OFF = 2000
#LIFT_TOP = -72
LIFT_TOP = -60
greenButtonHoldTime = StopWatch()
greenButtonDown = False
speed = 0

def runArm():
    remote.light.on(Color.RED)
    arm.run_target(SPEED_ARM, LIFT_TOP)
    arm.run_target(2*SPEED_ARM, LIFT_TOP+15)
    arm.run_target(2*SPEED_ARM, LIFT_TOP)
    arm.run_target(2*SPEED_ARM, LIFT_TOP+15)
    arm.run_target(2*SPEED_ARM, LIFT_TOP)
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
        speed = max(MIN_DC, min(100, speed+ACCELERATION))
    elif Button.LEFT_MINUS in buttons:
        speed = min(-MIN_DC, max(-100, speed-ACCELERATION))
    elif speed > 0:
        speed = max(0, speed - 2*ACCELERATION)
    else:
        speed = min(0, speed + 2*ACCELERATION)
    drive.dc(speed)

    # Steering:
    if Button.RIGHT_PLUS in buttons:
        steeringTarget = MIN_STEERING
    elif Button.RIGHT_MINUS in buttons:
        steeringTarget = MAX_STEERING
    else:
        steeringTarget = 0
    steeringDiff = steeringTarget-steer.angle()
    steerDC = min(100, max(-100, STEERING_BOOST*steeringDiff))
    if abs(steerDC) < 10:
        steerDC = 0
    steer.dc(steerDC)

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
