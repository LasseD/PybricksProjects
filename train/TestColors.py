from pybricks.pupdevices import DCMotor, ColorSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait, StopWatch

colors = [
    Color(h=21, s=65, v=100),
    Color(h=353, s=89, v=98),
    Color(h=354, s=70, v=65),
    Color(h=11, s=75, v=88),
    Color(h=19, s=62, v=94),
    Color(h=3, s=48, v=57),
    Color(h=195, s=15, v=31),
    Color(h=191, s=19, v=66),
    Color(h=197, s=20, v=97),
    Color(h=329, s=73, v=100),
    Color(h=0, s=0, v=100),
    Color(h=217, s=91, v=91),
    Color(h=213, s=59, v=48),
    Color(h=208, s=73, v=100),
    Color(h=180, s=75, v=100),
    Color(h=190, s=84, v=89),
    Color(h=167, s=37, v=43),
    Color(h=155, s=75, v=67),
    Color(h=155, s=43, v=89),
    Color(h=93, s=65, v=99),
    Color(h=60, s=31, v=100),
    Color(h=49, s=66, v=99),
    Color(h=41, s=66, v=100)
]
sensor = ColorSensor(Port.A)
sensor.detectable_colors(colors)

motor = DCMotor(Port.B)
motor.dc(50)
watch = StopWatch()

c1 = None
while True:
    c2 = sensor.color()
    if c1 != c2:
        c1 = c2
        print(watch.time(), c2)
    wait(20)
