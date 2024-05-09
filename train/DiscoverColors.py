from pybricks.pupdevices import ColorSensor
from pybricks.parameters import Color, Port
from pybricks.tools import wait

sensor = ColorSensor(Port.A)

while True:
    sensor.lights.on()
    wait(100)
    c = sensor.hsv()
    print('Color(h='+str(c.h)+', s='+str(c.s)+', v='+str(c.v) + '),')
    sensor.lights.off()
    wait(2000)
