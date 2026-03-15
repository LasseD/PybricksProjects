from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, TouchSensor
from pybricks.iodevices import DCMotor, AnalogSensor
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.tools import wait
from pybricks.pupdevices import Remote

hub = EV3Brick()
hub.screen.clear()
remote = Remote()

lift = Motor(Port.A)
boom = Motor(Port.D)
legs1 = DCMotor(Port.B)
legs2 = DCMotor(Port.C)

colorBoom = ColorSensor(Port.S1)
colorLift = ColorSensor(Port.S4)

LEGS_MAX = 60
LEGS_INC = 3
LEGS_MIN = 25
legs = 0
BOOM_SPEED = 380

#color = ColorSensor(Port.S1)
#light = AnalogSensor(Port.S1, custom=True)
while True:
    pressed = remote.buttons.pressed()
    ok = True
    #print("Boom", colorBoom.color())
    #print("Lift", colorLift.color())

    # Boom:
    if Button.LEFT_PLUS in pressed:
        if colorBoom.color() == Color.GREEN:
            ok = False
            boom.stop()
        else:
            boom.run(BOOM_SPEED)
    elif Button.LEFT_MINUS in pressed:
        if colorBoom.color() == Color.YELLOW:
            ok = False
            boom.stop()
        else:
            boom.run(-BOOM_SPEED)
    else:
        boom.stop()

    # Lift:
    c = colorLift.color()
    if Button.LEFT in pressed:
        if c != Color.YELLOW and c != Color.RED:
            lift.stop()
            ok = False
        else:
            lift.run(-500)
    elif Button.RIGHT in pressed:
        if c == Color.RED:
            lift.stop()
            ok = False
        else:
            lift.run(600)
    else:
        lift.stop()

    # Legs:
    if Button.RIGHT_PLUS in pressed:
        legs = legs + LEGS_INC
        if legs > LEGS_MAX:
            legs = LEGS_MAX
        elif legs < LEGS_MIN:
            legs = LEGS_MIN
    elif Button.RIGHT_MINUS in pressed:
        legs = legs - LEGS_INC
        if legs < -LEGS_MAX:
            legs = -LEGS_MAX
        elif legs > -LEGS_MIN:
            legs = -LEGS_MIN
    else:
        legs = 0
    legs1.dc(-legs)
    legs2.dc(legs)

    remote.light.on(Color.GREEN if ok else Color.RED)
    wait(60)
