from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, Motor, Remote
from pybricks.parameters import Color, Port, Stop, Button
from pybricks.tools import wait, StopWatch

hub = CityHub()
motor = DCMotor(Port.A)
decoupler = Motor(Port.B)
watch = StopWatch()

COUPLE_SPEED = 800
COUPLE_ANGLE = 365
TIME_ACCELERATE_MS = 2500
TIME_TURN_OFF = 5000
ACCELERATION = 6
MIN_DC = 21

# Reset by pulling the decoupler in to find a known position
def reset():
    hub.light.on(Color.YELLOW) # Indicating that the program on the hub is resetting
    decoupler.run_until_stalled(-300, then=Stop.COAST, duty_limit=38)
    decoupler.run_angle(COUPLE_SPEED, 36, Stop.COAST) # Move to free/released position
    decoupler.reset_angle(0) # Now angle 0 is decoupled position
    couple(True) # Default position is coupling ready
    hub.light.off() # Ready for commands

coupled = False
def couple(wait = False):
    global coupled
    decoupler.run_target(COUPLE_SPEED, COUPLE_ANGLE, Stop.BRAKE, wait)
    coupled = True

def decouple(wait = False):
    global coupled
    decoupler.run_target(COUPLE_SPEED, 0, Stop.COAST, wait)
    coupled = False

def runDecoupler():
    global coupled
    if not decoupler.done():
        return
    if coupled:
        decouple()
    else:
        couple()

remote = Remote()
reset()

timeout = 0 # When > 0, an action is being performed until watch.time() >= timeout
prev_target = 0
speed = 0
target = 0
greenButtonHoldTime = StopWatch()
greenButtonDown = False

# Set the speed based on current time and target sped
def update():
    global target, speed, prev_target, timeout

    t = watch.time()
    if timeout == 0: # Too little for slow acceleration:
        speed = target # Used for small corrections
    elif t < TIME_ACCELERATE_MS:
        speed = prev_target + (target-prev_target) * t / TIME_ACCELERATE_MS
    else:
        speed = target
    motor.dc(speed)

while True:
    wait(80)
    update()
    buttons = remote.buttons.pressed()

    # Slow Acceleration:
    commandAccepted = True
    if Button.LEFT in buttons or Button.RIGHT in buttons:
        target = 0
        timeout = 0
    elif Button.LEFT_PLUS in buttons:
        target = min(100, target+ACCELERATION)
        timeout = TIME_ACCELERATE_MS
    elif Button.RIGHT_PLUS in buttons:
        target = min(100, target+ACCELERATION)
        timeout = 0
    elif Button.LEFT_MINUS in buttons:
        target = max(-100, target-ACCELERATION)
        timeout = TIME_ACCELERATE_MS
    elif Button.RIGHT_MINUS in buttons:
        target = max(-100, target-ACCELERATION)
        timeout = 0
    else:
        commandAccepted = False

    if commandAccepted:
        if target > 0 and target < MIN_DC:
            if prev_target < 0 or prev_target > target:
                target = 0
            else:
                target = MIN_DC
        elif target < 0 and target > -MIN_DC:
            if prev_target > 0 or prev_target < target:
                target = 0
            else:
                target = -MIN_DC
        #print(target, prev_target)
        prev_target = target
        watch.reset()
        continue

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
                runDecoupler()
        greenButtonDown = False
