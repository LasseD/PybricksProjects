from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Direction, Port
from pybricks.tools import wait

# Hardware:
technicHub = TechnicHub()
technicHub.light.on(Color.RED)
remote = Remote()
technicHub.light.on(Color.GREEN)
motorL = Motor(Port.B)
motorR = Motor(Port.A, Direction.COUNTERCLOCKWISE)

while True:
    buttons = remote.buttons.pressed()

    if Button.LEFT_PLUS in buttons:
        motorL.dc(100)
    elif Button.LEFT_MINUS in buttons:
        motorL.dc(-100)
    else:
        motorL.dc(0)

    if Button.RIGHT_PLUS in buttons:
        motorR.dc(100)
    elif Button.RIGHT_MINUS in buttons:
        motorR.dc(-100)
    else:
        motorR.dc(0)

    # Turn off using green button:
    if Button.CENTER in buttons:
        technicHub.system.shutdown()

    wait(25)
