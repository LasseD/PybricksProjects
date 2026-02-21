from pybricks.hubs import CityHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Color, Direction, Port, Side
from pybricks.tools import wait

# Set up hardware:
hub = CityHub()
hub.light.on(Color.RED)
remote = Remote()
hub.light.on(Color.GREEN)
remote.light.on(Color.GREEN)
motors = [Motor(Port.B, Direction.COUNTERCLOCKWISE), Motor(Port.A)]

# Main loop:
steering = 0
speed = 0
MAX_SPEED = 100
MIN_SPEED = 10
SPEED_INC = 4
MAX_STEERING_SPEED = 80
STEERING_INC = 2
while True:
    buttons = remote.buttons.pressed()

    # Control speed with left side:
    if Button.LEFT_PLUS in buttons:
        speed = speed + SPEED_INC
        if speed > MAX_SPEED:
            speed = MAX_SPEED
    elif Button.LEFT_MINUS in buttons:
        speed = speed - SPEED_INC
        if speed < -MAX_SPEED:
            speed = -MAX_SPEED
    else:
        speed = speed * 0.9
        if abs(speed) < MIN_SPEED:
            speed = 0

    # Control steering with right side:
    if Button.RIGHT_PLUS in buttons:
        steering = max(0, steering + STEERING_INC)
        if steering > MAX_STEERING_SPEED:
            steering = MAX_STEERING_SPEED
    elif Button.RIGHT_MINUS in buttons:
        steering = min(0, steering - STEERING_INC)
        if steering < -MAX_STEERING_SPEED:
            steering = -MAX_STEERING_SPEED
    else:
        steering = steering * 0.9
        if abs(steering) < 3:
            steering = 0

    # Update motors:
    speed1 = max(-100, min(100, speed + steering))
    speed2 = max(-100, min(100, speed - steering))
    motors[0].dc(speed1)
    motors[1].dc(speed2)

    wait(25)
