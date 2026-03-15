from pybricks.hubs import CityHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Direction, Port
from pybricks.tools import wait

# Set up hardware:
hub = CityHub()
hub.light.on(Color.RED)
remote = Remote()
hub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)
m1 = Motor(Port.B, Direction.COUNTERCLOCKWISE)
m2 = Motor(Port.A)

# Main loop:
speed_left = 0
speed_right = 0
SPEED_INC = 22

def updateMotor(m, plus, minus, currentSpeed):
    if plus:
        currentSpeed = currentSpeed + SPEED_INC
        if currentSpeed > 100:
            currentSpeed = 100
    elif minus:
        currentSpeed = currentSpeed - SPEED_INC
        if currentSpeed < -100:
            currentSpeed = -100
    else:
        currentSpeed = currentSpeed * 0.6
        if abs(currentSpeed) < 30:
            m.stop()
            return 0
    m.dc(currentSpeed)
    return currentSpeed

while True:
    buttons = remote.buttons.pressed()
    speed_left = updateMotor(m1, Button.LEFT_PLUS in buttons, Button.LEFT_MINUS in buttons, speed_left)
    speed_right = updateMotor(m2, Button.RIGHT_PLUS in buttons, Button.RIGHT_MINUS in buttons, speed_right)
    wait(50)
