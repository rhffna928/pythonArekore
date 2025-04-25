from turtle import *
import colorsys
import random

def patten():
    tracer(25)
    pensize(25)

    h = 0.1
    bgcolor("white")
    lt(80)
    fd(180)
    lt(180)
    lt(80)
    for i in range(random.randint(110,330)):
        c = colorsys.hsv_to_rgb(h,0.50,0.777)
        color(c)
        h+=0.004
        fd(i)
        rt(50)
        rt(40)
        fd(500)
        rt(120)

for i in range(20):
    patten()