from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch, Matrix
from umath import *

hub = InventorHub()

class Marquee:
    def __init__(self, hub):
        self.display = hub.display
        self.DOTS = [
            ['AAA', 'BB ', ' CC', 'DD ', 'EEE', 'FFF', ' GG ', 'H H', 'III', 'JJJ', 'K  K', 'L  ', 'M   M', 'N   N', ' OO ', 'PPP ', ' QQ ', 'RRR ', 'SSS', 'TTT', 'U  U', 'V   V', 'W   W', 'X   X', 'Y   Y', 'ZZZZ', '000', ' 1 ', '222', '333', '4 4', '555', '666', '777', '888', '999', ' ', '   ', ' ', ' ', ' ', '  '],
            ['A A', 'B B', 'C  ', 'D D', 'E  ', 'F  ', 'G   ', 'H H', ' I ', '  J', 'K K ', 'L  ', 'MM MM', 'NN  N', 'O  O', 'P  P', 'Q  Q', 'R  R', 'S  ', ' T ', 'U  U', 'V   V', 'W   W', ' X X ', ' Y Y ', '   Z', '0 0', '11 ', '  2', '  3', '4 4', '5  ', '6  ', '  7', '8 8', '9 9', ':', '   ', ' ', ' ', ' ', '=='],
            ['AAA', 'BBB', 'C  ', 'D D', 'EE ', 'FF ', 'G GG', 'HHH', ' I ', '  J', 'KK  ', 'L  ', 'M M M', 'N N N', 'O  O', 'PPP ', 'Q  Q', 'RRR ', 'SSS', ' T ', 'U  U', 'V   V', 'W   W', '  X  ', '  Y  ', ' ZZ ', '0 0', ' 1 ', '222', '333', '444', '555', '666', '  7', '888', '999', ' ', '---', ' ', ' ', ' ', '  '],
            ['A A', 'B B', 'C  ', 'D D', 'E  ', 'F  ', 'G  G', 'H H', ' I ', 'J J', 'K K ', 'L  ', 'M   M', 'N  NN', 'O  O', 'P   ', 'Q QQ', 'R R ', '  S', ' T ', 'U  U', ' V V ', 'W W W', ' X X ', '  Y  ', 'Z   ', '0 0', ' 1 ', '2  ', '  3', '  4', '  5', '6 6', '  7', '8 8', '  9', ':', '   ', ' ', ',', ' ', '=='],
            ['A A', 'BB ', ' CC', 'DD ', 'EEE', 'F  ', ' GG ', 'H H', 'III', 'JJJ', 'K  K', 'LLL', 'M   M', 'N   N', ' OO ', 'P   ', ' Q Q', 'R  R', 'SSS', ' T ', ' UU ', '  V  ', ' W W ', 'X   X', '  Y  ', 'ZZZZ', '000', '111', '222', '333', '  4', '555', '666', '  7', '888', '  9', ' ', '   ', '.', ',', ' ', '  ']
        ]
        CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:-., ='
        self.map = {}
        for i in range(0, len(CHARS)):
            c = CHARS[i]
            self.map[c] = i
    def show(self, text, interval):
        # Set up pixels:
        self.PIXELS = [[], [], [], [], []]
        for i in range(0, len(text)):
            c = text[i]
            dotIdx = self.map[c]
            for row in range(0, 5):
                s = self.DOTS[row][dotIdx]
                for j in range(0, len(s)):
                    self.PIXELS[row].append(s[j])
                self.PIXELS[row].append(' ')
        # Build animation:
        matrices = []
        for x in range(0, len(self.PIXELS[0])):
            m = []
            for y in range(0, 5):
                row = []
                for xx in range(0, 5):
                    letter = self.PIXELS[y][(x+xx)%len(self.PIXELS[y])]
                    row.append(100 if letter != ' ' else 0)
                m.append(row)
            matrices.append(Matrix(m))
        self.display.animate(matrices, interval)

hub.display.orientation(Side.RIGHT)
m = Marquee(hub)
cnt = 0
#m.write('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:-.,')
timer = StopWatch()
while True:
    t = floor(timer.time()/1000)
    SS = t % 60
    t = floor(t/60)
    MM = t % 60
    H = floor(t/60)
    s = str(MM) + ':' + str(SS)
    if H > 0:
        s = str(H) + ':' + s 
    m.show('  TIME=' + s + '  COUNT=' + str(cnt), 200)
    if Button.RIGHT in hub.buttons.pressed():
        cnt = cnt + 1
    wait(20000)
