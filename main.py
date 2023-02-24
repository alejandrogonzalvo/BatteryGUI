from collections import deque

import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams
from matplotlib.animation import FuncAnimation

import numpy as np
from perlin_noise import PerlinNoise

import serial

BATTERIES = 6
TEMPERATURES = 4
HISTORY = 200

def configure_serial():
    ser = serial.Serial("/dev/ttyUSB0")
    ser.baudrate = 115200
    ser.port = COM0
    ser.open()

def configure_style():
    COLOR = 'white'
    rcParams['text.color'] = COLOR
    rcParams['axes.labelcolor'] = COLOR
    rcParams['xtick.color'] = COLOR
    rcParams['ytick.color'] = COLOR

    rcParams['xtick.major.pad']='8'
    rcParams['ytick.major.pad']='8'

def configure_voltage_axis(vax):
    vax = plt.subplot(gs[2*i:2*i+2, 0])
    vax.yaxis.tick_right()
    vax.set_ylim([23, 25])
    vax.margins(x=0)
    vax.axes.get_xaxis().set_visible(False)
    vax.set_facecolor("#003B4D")

def configure_temperature_axis(tax):
    tax = plt.subplot(gs[i*3:i*3+3, 1])
    tax.set_ylim([3.3, 4.2])
    tax.margins(x=0)
    tax.axes.get_xaxis().set_visible(False)
    tax.axes.get_yaxis().set_visible(False)
    tax.set_facecolor("#003B4D")

# function that draws each frame of the animation
def animate(i):

    voltages = list(map(float, ser.readline().strip().split(" ")))
    for j in range(BATTERIES):
        y[j].append(voltages(j))
        y[j].popleft()
        lines[j].set_data(x, y[j])
        voltage_axis[j].set_yticks([voltages(j)])

    for j in range(TEMPERATURES):
        tlines[j].set_data(x, y[j])

def add_logo():
    im = plt.imread('logo.png')
    newax = fig.add_axes([0.82, 0.85, 0.2, 0.2], anchor='NE', zorder=-1)
    newax.imshow(im)
    newax.axis('off')

def run_animation():
    ani = FuncAnimation(fig, animate, interval=15, repeat=False)


if __name__ == "__main__":
    configure_serial()
    configure_style()

    x = deque([i for i in range(HISTORY)])
    y = deque([24*HISTORY]) * BATTERIES


    # create the figure and axes objects
    fig = plt.figure(facecolor='#001f29')

    gs = fig.add_gridspec(12, 2)

    voltage_axis = [0]*BATTERIES
    lines = [0]*BATTERIES
    for i in range(BATTERIES):
        configure_voltage_axis(voltage_axis[i])
        lines[i] = voltage_axis[i].plot(x, y[i])[0]

    voltage_axis[0].set_title("Battery Cells", size=36, color="white", pad=20)

    temperature_axis = [0]*TEMPERATURES
    tlines = [0]*TEMPERATURES
    for i in range(TEMPERATURES):
        configure_temperature_axis(temperature_axis[i])
        tlines[i] = temperature_axis[i].plot(x, y[i])[0]
    temperature_axis[0].set_title("Battery temperatures", size=36, color="white", pad=20)
    
    add_logo()
    run_animation()


    plt.subplots_adjust(left=0.02, bottom=0.02, right=0.98, wspace=0.1, hspace=0.3)
    plt.show()
