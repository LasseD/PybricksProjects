from pybricks.pupdevices import Light
from pybricks.parameters import Port
from pybricks.tools import wait

lights = [Light(Port.A), Light(Port.B), Light(Port.C), Light(Port.D)]
values = [5, 10, 20, 30, 45, 60, 80, 100, 90, 80, 60, 40, 35, 30, 5, 35, 55, 80, 60, 40, 75, 100, 75, 50, 25, 10]
j = 0

while True:
    for i in range(4):
        v = values[(i+j)%len(values)]
        lights[i].on(v)
        wait(40)
        j = j + 1
