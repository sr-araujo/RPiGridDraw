# Python program created with 8x8grid-sense.py
from sense_hat import SenseHat
import time

# Color Tuples
E  = (  0,   0,   0) # Empty (Black or LED off)
R  = (255,   0,   0) # Red
O  = (255, 128,   0) # Orange
Y  = (255, 255,   0) # Yellow
G  = (  0, 128,   0) # Green
C  = (  0, 255, 255) # Cyan
B  = (  0,   0, 255) # Blue
P  = (102,   0, 204) # Purple
K  = (255,   0, 255) # Pink
W  = (255, 255, 255) # White

sh = SenseHat()
frames = [
    [
    R,K,P,B,C,G,Y,O,
    O,R,K,P,B,C,G,Y,
    Y,O,R,K,P,B,C,G,
    G,Y,O,R,K,P,B,C,
    C,G,Y,O,R,K,P,B,
    B,C,G,Y,O,R,K,P,
    P,B,C,G,Y,O,R,K,
    K,P,B,C,G,Y,O,R
    ]
]

for x in frames:
    sh.set_pixels(x)
    time.sleep(0.25)

input('Press ENTER to continue. .  .')
sh.clear()