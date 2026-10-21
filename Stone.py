from pybricks.pupdevices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

stones12 = Motor(Port.C)
stones34 = Motor(Port.A)
guy = Motor(Port.B)
sensor = UltrasonicSensor(Port.D)
watch = StopWatch()
STONE_SPEED = 600
STONE_ANGLE = 35
GUY_SPEED_SLOW = 300
GUY_SPEED_FAST = 800
GUY_ANGLE_NEUTRAL = -30
GUY_ANGLE_ADD = -25

# reset:
guy.run_target(GUY_SPEED_SLOW, GUY_ANGLE_NEUTRAL, Stop.COAST)
stones12.run_target(STONE_SPEED, 0, Stop.COAST)
stones34.run_target(STONE_SPEED, 0, Stop.COAST)
lastDistance = sensor.distance()
print('Default distance:', lastDistance)
aim = 0
sensor.lights.on(100)
wait(300)
sensor.lights.off()

def throw(x):
    if x == 0:
        return
    guy.run_target(GUY_SPEED_FAST, GUY_ANGLE_NEUTRAL, Stop.COAST, False)
    wait(220)
    if x >= 1:
        stones12.run_target(STONE_SPEED, -STONE_ANGLE, Stop.COAST)
    if x == 1:
        stones12.run_target(STONE_SPEED, 0, Stop.COAST)
    else:
        stones12.run_target(STONE_SPEED, STONE_ANGLE, Stop.COAST)
        stones12.run_target(STONE_SPEED, 0, Stop.COAST, x == 2)
    if x >= 3:
        stones34.run_target(STONE_SPEED, -STONE_ANGLE, Stop.COAST)
        if x == 3:
            stones34.run_target(STONE_SPEED, 0, Stop.COAST)
        else:
            stones34.run_target(STONE_SPEED, STONE_ANGLE, Stop.COAST)
            stones34.run_target(STONE_SPEED, 0, Stop.COAST)

def demo():
    guy.run_angle(GUY_SPEED_SLOW, 4 * GUY_ANGLE_ADD, Stop.COAST)
    throw(4)

watch.reset()
while True:
    wait(300)
    if aim == 0 and watch.time() > 45000:
        demo()
        watch.reset()
    d = sensor.distance()
    print(watch.time(), d)
    if (d != 2000 and d >= lastDistance) or (lastDistance == 2000 and d != 2000):
        guy.run_angle(GUY_SPEED_SLOW, GUY_ANGLE_ADD, Stop.COAST)
        aim = aim + 1
        sensor.lights.on(25*aim)
        if aim == 4:
            throw(4)
            aim = 0
        watch.reset()
    else:
        sensor.lights.off()
        throw(aim)
        aim = 0
    lastDistance = d
