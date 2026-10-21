from pybricks.hubs import EssentialHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Axis, Color, Port
from pybricks.tools import wait

# Hardware:
hub = EssentialHub()
motor = Motor(Port.B)
#remote = Remote()

# Source code and PID tuning by Ole Caprani:
# https://cs.au.dk/~ocaprani/legolab/Danish.dir/FLLprogrammering/SorteStreger/LeftEdgeDrive/PID%20Controller%20For%20Lego%20Mindstorms%20Robots.pdf
Kc = 0.079 # Critical gain
dT = 0.050 # Loop time ms
# Multipliers for PID variables:
Kd = 0.3
Kp = 0.45
Ki = 0.25
#Kd = 0.3
#Kp = 0.45
#Ki = 0.25

# Specific for roller skate:
MIN_POWER = 11#21 # Found using findMinimalMovementPower()

def getPosition():
    return hub.imu.rotation(Axis.Z)

integral = 0
lastError = 0
adjust = 0.2
enabled = True
motor.reset_angle(0)
targetPosition = getPosition()


while True:
    buttons = [] #remote.buttons.pressed()
    if enabled:
        p = getPosition()
        error = (p-targetPosition + motor.angle()/100) / dT
        integral = integral + error
        derivative = error - lastError
        v = Kp*error + Ki*integral + Kd*derivative
        v = v + MIN_POWER if v > 0 else v - MIN_POWER
        motor.dc(v)
        lastError = error

    if Button.CENTER in buttons: # Switch mode and reset:
        enabled = not enabled
        motor.reset_angle(0)
        motor.dc(0)
        targetPosition = getPosition()
        integral = 0
        lastError = 0
        hub.light.on(Color.RED if not enabled else Color.GREEN)
        wait(1000)
    if Button.LEFT in buttons:
        hub.system.shutdown()
    if Button.LEFT_PLUS in buttons:
        targetPosition = targetPosition - adjust
    elif Button.LEFT_MINUS in buttons:
        targetPosition = targetPosition + adjust
#       print('G P',error,'I',integral,'D',derivative,'V',v,'Target',targetPosition,adjust)
    wait(dT*1000)
