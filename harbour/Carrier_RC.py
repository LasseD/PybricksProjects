from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Light, Remote
from pybricks.parameters import Button, Color, Direction, Port
from pybricks.tools import wait, StopWatch

MAX_TRACK = 70
MIN_LIFT_DOWN = -70
MAX_LIFT_UP = 100
SPEED_INC = 20
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

def updateMotor(m, plus, minus, currentSpeed, mn, mx):
    if plus:
        currentSpeed = currentSpeed + SPEED_INC
        if currentSpeed > mx:
            currentSpeed = mx
    elif minus:
        currentSpeed = currentSpeed - SPEED_INC
        if currentSpeed < mn:
            currentSpeed = mn
    else:
        currentSpeed = currentSpeed * 0.6
        if abs(currentSpeed) < 30:
            m.stop()
            return 0
    m.dc(currentSpeed)
    return currentSpeed

while True:
    updateFlash()
    buttons = remote.buttons.pressed()
    speed_left = updateMotor(m1, Button.LEFT_PLUS in buttons, Button.LEFT_MINUS in buttons, speed_left, -MAX_TRACK, MAX_TRACK)
    speed_right = updateMotor(m2, Button.RIGHT_PLUS in buttons, Button.RIGHT_MINUS in buttons, speed_right, -MAX_TRACK, MAX_TRACK)
    speed_lift = updateMotor(lifter, Button.LEFT in buttons, Button.RIGHT in buttons, speed_lift, MIN_LIFT_DOWN, MAX_LIFT_UP)
    wait(50)
