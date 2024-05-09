from pybricks.hubs import EssentialHub
from pybricks.pupdevices import DCMotor, ColorSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch

Color.ORANGE = Color(h=21, s=65, v=100) # Marker
Color.RED = Color(h=353, s=89, v=98) # Fast
Color.BLUE = Color(h=217, s=91, v=91) # Slow
Color.GREEN = Color(h=155, s=75, v=67) # Stop for station
Color.LIME = Color(h=93, s=65, v=99) # Reverse
colors = [
    Color.ORANGE,
    Color.RED,
    Color.BLUE,
    Color.GREEN,
    Color.LIME,
    Color(h=354, s=70, v=65),
    Color(h=11, s=75, v=88),
    Color(h=19, s=62, v=94),
    Color(h=3, s=48, v=57),
    Color(h=195, s=15, v=31),
    Color(h=191, s=19, v=66),
    Color(h=197, s=20, v=97),
    Color(h=329, s=73, v=100),
    Color(h=0, s=0, v=100),
    Color(h=213, s=59, v=48),
    Color(h=208, s=73, v=100),
    Color(h=180, s=75, v=100),
    Color(h=190, s=84, v=89),
    Color(h=167, s=37, v=43),
    Color(h=155, s=43, v=89),
    Color(h=60, s=31, v=100),
    Color(h=49, s=66, v=99),
    Color(h=41, s=66, v=100),
    Color(h=197, s=22, v=57),
    Color(h=21, s=55, v=86),
    Color(h=190, s=11, v=55),
    Color(h=40, s=46, v=85)
]
sensor = ColorSensor(Port.A)
sensor.detectable_colors(colors)
hub = EssentialHub(broadcast_channel=1)

PRW_FAST = 55
PWR_SLOW = 35
pwr = PRW_FAST
watch = StopWatch()

motor = DCMotor(Port.B)
motor.dc(pwr)

def accelerateTo(p, timeMS = 750):
    global pwr, watch
    watch.reset()
    while watch.time() < timeMS:
        motor.dc(pwr + (p-pwr)*(watch.time()/timeMS))
        wait(50)
    pwr = p

while True:
    c = sensor.color()
    if c == Color.ORANGE:
        watch.reset()
        while watch.time() < 200: # Expect second color:
            c = sensor.color()
            if c == Color.RED:
                accelerateTo(PRW_FAST if pwr >= 0 else -PRW_FAST)
                break
            elif c == Color.BLUE:
                accelerateTo(PWR_SLOW if pwr >= 0 else -PWR_SLOW)
                break
            elif c == Color.GREEN:
                prev_pwr = pwr
                accelerateTo(0)
                hub.ble.broadcast(42) # Open door command 42
                wait(1000)
                hub.ble.broadcast(0)
                wait(8000)
                accelerateTo(prev_pwr)
                break
            elif c == Color.LIME:
                accelerateTo(-pwr)
                break
            wait(20)        
    wait(20)
