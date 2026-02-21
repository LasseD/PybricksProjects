from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Light, Remote
from pybricks.parameters import Button, Color, Direction, Port
from pybricks.tools import wait, StopWatch

# Lifter constants:
SPEED_MAX = 500
SPEED_INC = 25
LIFT_MAX = 800
LIFT_INC = 20
# Track constants:
m1 = Motor(Port.B, Direction.COUNTERCLOCKWISE)
m2 = Motor(Port.A)

hub = TechnicHub()
flashWatch = StopWatch()
flash = Light(Port.C)
lifter = Motor(Port.D)

hub.light.on(Color.RED)
remote = Remote()
hub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)

def updateFlash():
    ms = flashWatch.time()
    if ms % 650 < 70:
        flash.on(100)
    else:
        flash.off()

speed_left = 0
speed_right = 0
speed_lift = 0

def updateMotor(m, plus, minus, currentSpeed, speedInc, speedMax):
    if plus:
        currentSpeed = currentSpeed + speedInc
        if currentSpeed > speedMax:
            currentSpeed = speedMax
    elif minus:
        currentSpeed = currentSpeed - speedInc
        if currentSpeed < -speedMax:
            currentSpeed = -speedMax
    else:
        currentSpeed = currentSpeed * 0.6
        if abs(currentSpeed) < 10:
            m.stop()
            return 0
    m.run(currentSpeed)
    return currentSpeed

while True:
    updateFlash()
    buttons = remote.buttons.pressed()
    speed_left = updateMotor(m1, Button.LEFT_PLUS in buttons, Button.LEFT_MINUS in buttons, speed_left, SPEED_INC, SPEED_MAX)
    speed_right = updateMotor(m2, Button.RIGHT_PLUS in buttons, Button.RIGHT_MINUS in buttons, speed_right, SPEED_INC, SPEED_MAX)
    speed_lift = updateMotor(lifter, Button.LEFT in buttons, Button.RIGHT in buttons, speed_lift, LIFT_INC, LIFT_MAX)

    wait(25)
