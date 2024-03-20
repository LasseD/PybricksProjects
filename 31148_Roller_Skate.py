from pybricks.hubs import EssentialHub
from pybricks.pupdevices import Motor, Remote
from pybricks.parameters import Button, Axis, Color, Port
from pybricks.tools import wait

hub = EssentialHub()
remote = Remote()
motorSteering = Motor(Port.A)
motor = Motor(Port.B)

# Source code and PID tuning by Ole Caprani:
# https://cs.au.dk/~ocaprani/legolab/Danish.dir/FLLprogrammering/SorteStreger/LeftEdgeDrive/PID%20Controller%20For%20Lego%20Mindstorms%20Robots.pdf
Kc = 0.079 # Critical gain
dT = 0.050 # Loop time ms
# Multipliers for PID variables:
Kd = 0.10
Kp = 0.21
Ki = 0.21
#Kd = 0.19
#Kp = 0.38
#Ki = 0.24
#Kd = 0.09
#Kp = 0.28
#Ki = 0.24

MIN_POWER = 11
MAX_STEERING = 12

def getPosition():
    return hub.imu.rotation(Axis.Z)

integral = 0
lastError = 0
enabled = False
motor.reset_angle(0)
targetPosition = getPosition()

while True:
    buttons = remote.buttons.pressed()
    if enabled:
        p = getPosition()
        error = (p-targetPosition + motor.angle()/100) / dT
        integral = integral + error
        derivative = error - lastError
        v = Kp*error + Ki*integral + Kd*derivative
        v = v + MIN_POWER if v > 0 else v - MIN_POWER
        motor.dc(v)
        lastError = error
    else:
        if Button.LEFT_PLUS in buttons:
            speed = -100
        elif Button.LEFT_MINUS in buttons:
            speed = 100
        else:
            speed = 0
        motor.dc(speed)

    if Button.CENTER in buttons: # Switch mode and reset:
        motor.reset_angle(0)
        motor.dc(0)
        targetPosition = getPosition()
        integral = 0
        lastError = 0
        hub.light.on(Color.RED if not enabled else Color.GREEN)
        if enabled:
            motor.dc(100)
            wait(200)
            motor.dc(0)
        wait(500)
        enabled = not enabled
        if Button.CENTER in remote.buttons.pressed():
            hub.system.shutdown()

    # Steering:
    if Button.RIGHT_PLUS in buttons:
        steeringTarget = -MAX_STEERING
    elif Button.RIGHT_MINUS in buttons:
        steeringTarget = MAX_STEERING
    else:
        steeringTarget = 0
    motorSteering.track_target(steeringTarget)

    wait(dT*1000)
