from pybricks.hubs import TechnicHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Side
from pybricks.tools import wait

# Set up hardware:
technicHub = TechnicHub()
technicHub.light.on(Color.RED)
remote = Remote()
technicHub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)
motors = [Motor(Port.B), Motor(Port.A, Direction.COUNTERCLOCKWISE)]

# Main loop:
steering = 0
STEERING_SPEED = 20
while True:
    buttons = remote.buttons.pressed()

    # Control speed with left side:
    speed = 0
    if Button.LEFT_PLUS in buttons:
        speed = 100
    elif Button.LEFT_MINUS in buttons:
        speed = -100

    # Control steering with right side:
    if Button.RIGHT_PLUS in buttons:
        steering = max(0, steering + STEERING_SPEED)
    elif Button.RIGHT_MINUS in buttons:
        steering = min(0, steering - STEERING_SPEED)
    else:
        steering = 0

    # Update motors:
    speed1 = max(-100, min(100, speed + steering))
    speed2 = max(-100, min(100, speed - steering))
    if technicHub.imu.up() == Side.TOP:
        motors[0].dc(speed1)
        motors[1].dc(speed2)
    else:
        motors[0].dc(-speed2)
        motors[1].dc(-speed1)

    # Turn off using green button:
    if Button.CENTER in buttons:
        technicHub.system.shutdown()

    wait(25)
