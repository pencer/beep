#!/usr/bin/python3
#coding:utf-8

#import RPi.GPIO as GPIO
import pigpio

import time
#import math
import sys
import keyboard
import random

A4 = 440
A4s = 466
B4 = 494
C1 = 33
C2 = 65
C3 = 131
C4 = 262
C5 = 523
C6 = 1047
C7 = 2093
C8 = 4186
Cs1 = 35
Cs2 = 69
Cs3 = 139
Cs4 = 277
Cs5 = 554
Cs6 = 1109
Cs7 = 2217
Cs8 = 4435
D1 = 37
D2 = 73
D3 = 147
D4 = 294
D5 = 587
D6 = 1175
D7 = 2349
D8 = 4699
Ds1 = 39
Ds2 = 78
Ds3 = 156
Ds4 = 311
Ds5 = 622
Ds6 = 1245
Ds7 = 2489
Ds8 = 4978
E1 = 41
E2 = 82
E3 = 165
E4 = 330
E5 = 659
E6 = 1319
E7 = 2637
E8 = 5274
F1 = 44
F2 = 87
F3 = 175
F4 = 349
F5 = 698
F6 = 1397
F7 = 2794
F8 = 5588
Fs1 = 46
Fs2 = 92
Fs3 = 185
Fs4 = 370
Fs5 = 740
Fs6 = 1480
Fs7 = 2960
Fs8 = 5920
G1 = 49
G2 = 98
G3 = 196
G4 = 392
G5 = 784
G6 = 1568
G7 = 3136
G8 = 6272
Gs1 = 52
Gs2 = 104
Gs3 = 208
Gs4 = 415
Gs5 = 831
Gs6 = 1661
Gs7 = 3322
Gs8 = 6645
A1 = 55
A2 = 110
A3 = 220
A4 = 440
A5 = 880
A6 = 1760
A7 = 3520
A8 = 7040
As1 = 58
As2 = 117
As3 = 233
As4 = 466
As5 = 932
As6 = 1865
As7 = 3729
As8 = 7459
B1 = 62
B2 = 123
B3 = 247
B4 = 494
B5 = 988
B6 = 1976
B7 = 3951
B8 = 7902

Z1 = 0
Z2 = 0
Z3 = 0
Z4 = 0
Z5 = 0
Z6 = 0
Z7 = 0
Z8 = 0

SET_SPEED = -1
WAVE = -2

speed_factor = 0.5
N16 = 0.1
N16f = 0.15
N8 = 0.2
N8f = 0.3
N4 = 0.4
N4f = 0.6
N2 = 0.8
N2f = 1.2
N1 = 1.6
delta = 0.02

sounds = [
#sound0
 [
  (Fs5, N4), (D5, N4), (A4, N4), (D5, N4), (E5, N4), (A5, N4), (Z5, N4),
  (A4, N4), (E5, N4), (Fs5, N4), (E5, N4), (A4, N4), (D5, N4),
 ],

#sound1
 [
  (Fs4, N4), (A4, N4), (E4, N4), (A4, N4),
  (Z4, N4), (Z4, N4), (Z4, N4), (Z4, N4),
  (Fs4, N4), (A4, N4), (E4, N4), (D4, N4),
  (Z4, N4), (Z4, N4), (Z4, N4), (Z4, N4),
  (Fs4, N4), (A4, N4), (E4, N4), (A4, N4),
  (Z4, N4), (Z4, N4), (Z4, N4), (Z4, N4),
  (Fs4, N4), (A4, N4), (E4, N4), (D4, N4),
  (Z4, N4), (Z4, N4), (Z4, N4), (Z4, N4),
 ],

#sound2 : Mario
 [
  (E4, N8), (E4, N8), (Z4, N8), (E4, N8), (Z4, N8),
  (C4, N8), (E4, N8), (Z4, N8), (G4, N8), (Z4, N8),
  (Z4, N8), (Z4, N8), (G3, N8), (Z4, N8), (Z4, N8), (Z4, N8),
  (C4, N8), (Z4, N4), (G3, N8), (Z3, N4), (E3, N8), (Z3, N4), (Z3, N8),
  (A3, N8), (Z4, N8), (B3, N8), (Z4, N8), (As3, N8), (A3, N8), (Z3, N8),
  (G3, N8), (C4, N8), (E4, N8), (G4, N8), (A4, N8), (Z3, N8),
  (F4, N8), (G4, N8), (Z4, N8), (E4, N8), (Z4, N8), (C4, N8),
  (Z4, N8), (D4, N8), (B3, N8), 
 ],

#sound3
 [
  (SET_SPEED, 0.9),
  (E4, N8), (A4, N4), (C5, N8), (E5, N2), 
  (E4, N8), (Gs4, N4), (B4, N8), (E5, N2), (Z4, N8),
  (E5, N8), (F5, N8), (E5, N8), (G5, N8), (G5, N8), (G5, N8), (F5, N8),
  (E5, N8), (D5, N8), (E5, N8), (D5, N8), 
 ],

#sound4
 [
  (C3, N8), (G3, N8), (C4, N8), (G3, N8),
  (C3, N8), (G3, N8), (C4, N8), (G3, N8),
  (C3, N8), (G3, N8), (C4, N8), (G3, N8),
  (C3, N8), (G3, N8), (C4, N8), (G3, N8),

  (C4, N8), (G4, N8), (C5, N8), (G4, N8),
  (C4, N8), (G4, N8), (C5, N8), (G4, N8),
  (C4, N8), (G4, N8), (C5, N8), (G4, N8),
  (C4, N8), (G4, N8), (C5, N8), (G4, N8),

  (C5, N8), (G5, N8), (C6, N8), (G5, N8),
  (C5, N8), (G5, N8), (C6, N8), (G5, N8),
  (C5, N8), (G5, N8), (C6, N8), (G5, N8),
  (C5, N8), (G5, N8), (C6, N8), (G5, N8),
 ],

#sound5
 [
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),

  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  #
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (G5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),

  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  (A5, N8), (E5, N8), (D5, N8), (C5, N8), (D5, N8), (E5, N8),
  #
  (G5, N8), (E5, N8), (C5, N8), (As4, N8), 
  (C5, N8), (E5, N8), (E5, N8), (G5, N8), 
  (C6, N8), (G5, N8), (C5, N8), (D6, N8), (E6, N8), 
 ],

#sound6
 [
  (WAVE, 0.9),
 ],

#sound7
 [
  (SET_SPEED, 0.9),
  (E4, N8), (A4, N4), (C5, N8), (E5, N2), 
  (E4, N8), (Gs4, N4), (B4, N8), (E5, N2), 
  (E5, N8), (F5, N8), (E5, N8), (G5, N8), 
  (G5, N8), (G5, N4), (F5, N8), (E5, N8), 
  (D5, N8), (E5, N8), (D5, N2), 
 ],

#sound8
 [
  (SET_SPEED, 0.9),
  (A4, N4), (F5, N1), (Z5, N8), (F5, N8), (G5, N8), (A5, N8), 
  (B5, N8), (A5, N8), (G5, N8), 
  (F5, N8), (E5, N1),
 ],

#sound9
# Chijou no hoshi
 [
  (SET_SPEED, 1.2),

  (A4, N8), 
  (D5, N8),
  (D5, N8), 
  (E5, N8),
  (E5, N8), 
  (F5, N8),
  (E5, N8f), 
  (D5, N16),
  (C5, N2), 
  (Z5, N4), 

  (F4, N8), 
  (As4, N8),
  (As4, N8), 
  (C5, N8),
  (C5, N8), 
  (D5, N8),
  (C5, N8f), 
  (As4, N16),
  (A4, N2), 
  (Z5, N4), 
 ],

#sound10
 [
  (SET_SPEED, 0.7),

  (D2, N8), 
  (C2, N8),
  (D2, N8), 
  (C2, N8),
  (D2, N8), 
  (C2, N8),
  (D2, N8), 
  (C2, N8),
  (F2, N2),
  (C2, N8),

 ],

#sound11
 [
  (SET_SPEED, 0.9),

  (A4, N4f), 
  (C5, N8),
  (C5, N8), 
  (As4, N8),
  (A4, N4), 
  (As4, N4),
  (A4, N4), 
  (E4, N4),
  (G4, N8),
  (F4, N4f),
  (Z4, N4),

  (F4, N8),
  (F4, N8),
  (G4, N8),
  (A4, N8),
  (As4, N4),
  (A4, N4),
  (C5, N8),
  (A4, N8),
  (G4, N8),
  (A4, N8),
  (F4, N4),

 ],

#sound12
# Amatsusoramiyo
 [
  (SET_SPEED, 0.5),

  (C5, N4),
  (C5, N4),
  (G4, N4),
  (A4, N4),
  (F4, N4),
  (G4, N4),
  (E4, N2),

  (G4, N4),
  (G4, N4),
  (C5, N4),
  (C5, N4),
  (E5, N4),
  (D5, N8),
  (C5, N8),
  (D5, N2),

  (E5, N4),
  (E5, N4),
  (D5, N4),
  (D5, N4),
  (C5, N4),
  (C5, N4),
  (A4, N2),

  (G4, N4),
  (C5, N4),
  (E5, N4),
  (D5, N8),
  (E5, N8),
  (D5, N2),
  (C5, N8),
  (G4, N8),
  (G4, N8),
  (G4, N8),

  (C5, N2),
  (Z5, N8),
  (C5, N8),
  (B4, N8),
  (A4, N8),
  (G4, N2),
  (C4, N4),

  (C4, N8),
  (G4, N8),
  (A4, N2),
  (Z4, N8),
  (F4, N8),
  (E4, N8),
  (E4, N8),
  (G4, N2),

 ],

#sound13
 [
  (SET_SPEED, 0.9),

  (C5, N4),
  (F5, N2),
  (Z5, N8),
  (E5, N8),
  (F5, N8),
  (G5, N8),
  (F5, N2),
  (C5, N4),
  (C5, N8),
  (C5, N8),

  (A5, N2),
  (Z5, N8),
  (Gs5, N8),
  (A5, N8),
  (As5, N8),
  (A5, N2),
  (F5, N4),
  (F5, N8),
  (F5, N8),

  (As5, N2),
  (Z5, N8),
  (D6, N8),
  (C6, N8),
  (As5, N8),
  (C6, N2),
  (A5, N4),
  (As5, N8),
  (As5, N8),

  (A5, N2),
  (Z5, N8),
  (G5, N8),
  (F5, N8),
  (E5, N8),
  (F5, N2),

 ],

]



pin = 12
led = 18

duty = 50
mode = 0
calibration = False

idx = 1
numarg = len(sys.argv)
while idx < numarg:
    key = sys.argv[idx]
    if key == "-h":
        print("Usage: script <mode>")
        exit()
    elif key == "-d":
        if (idx+1 <= numarg):
            duty = int(sys.argv[idx+1])
            print(f"duty={duty}")
            idx += 1
    elif key == "-m":
        if (idx+1 <= numarg):
            mode = int(sys.argv[idx+1])
            print(f"mode={mode}")
            idx += 1
    elif key == "-c":
        calibration = True
    else:
        print("Usage: script <mode>")
        exit()
    idx += 1

if calibration:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin,GPIO.OUT,initial=GPIO.LOW)
    val = 0
    print("Please input target key (ex. A4)")
    s = input().strip()
    if s != "":
        base = eval(s)
        print(f"Target Key '{s}': base freq = {base}")
    p = GPIO.PWM(pin,1)
    p.start(duty)
    p.ChangeFrequency(base + val)
    while True:
        key = input().strip()
        #key = keyboard.read_key()
        if key == "":
            print("empty")
            time.sleep(0.1)
            continue
        if key == "j":
            val += 1
            p.ChangeFrequency(base + val)
            print(f"Target Key '{s}': base freq = {base+val}")
            print("k")
        if key == "k":
            val -= 1
            p.ChangeFrequency(base + val)
            print(f"Target Key '{s}': base freq = {base+val}")
            print("k")
        if key == "q":
            break
        time.sleep(0.5)
        continue
        if keyboard.is_pressed('j'):
            val += 1
            p.ChangeFrequency(base + val)
            print(f"Target Key '{s}': base freq = {base}")
        elif keyboard.is_pressed('k'):
            val -= 1
            p.ChangeFrequency(base + val)
            print(f"Target Key '{s}': base freq = {base}")
        elif keyboard.is_pressed('q'):
            break
        time.sleep(0.5)
    p.stop()
    GPIO.cleanup()
    exit()

gpio = pigpio.pi()
gpio.set_mode(pin, pigpio.OUTPUT)
gpio.set_mode(led, pigpio.OUTPUT)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(pin,GPIO.OUT,initial=GPIO.LOW)
#GPIO.setup(led,GPIO.OUT,initial=GPIO.LOW)

#p = GPIO.PWM(pin,1)
#p.start(duty)

def gen_tone(pin, freq, sec):
    if freq <= 0:
        sleep(sec)
    else:
        period = 1.0 / freq
        h_period = 0.5 / freq
        n_repeat = int(sec * freq)
        for i in range(n_repeat):
            gpio.write(pin, 1)
            time.sleep(h_period)
            gpio.write(pin, 0)
            time.sleep(h_period)

num_sounds = len(sounds)
if mode == 0:
    mode = int(random.random() * num_sounds)
try:
    stop = False
    #GPIO.output(led, 1)
    gpio.write(led, 1)
    sound = sounds[mode % num_sounds]
    print(mode)
    print(mode % num_sounds)
    for (freq, length) in sound:
        if freq > 0:
            gpio.hardware_PWM(pin, freq, 500000)
            #gen_tone(pin, freq, length)
            #gpio.set_PWM_frequency(pin, freq)
            #gpio.set_PWM_range(pin, 100)
            #gpio.set_PWM_dutycycle(pin, duty)
            #p.ChangeDutyCycle(duty)
            #p.ChangeFrequency(freq * 1.00)
        elif freq == SET_SPEED:
            speed_factor = length
            continue
        elif freq == WAVE:
            _m12 = 1.0594630943592952645618252949463
            for c in range(4):
                freq = 220*1
                for r in range(1,32):
                    freq *= _m12
                    gpio.hardware_PWM(pin, int(freq), 500000)
                    time.sleep(0.02)
            continue
        else:
            gpio.hardware_PWM(pin, freq, 000000)
            #gpio.set_PWM_dutycycle(pin, 0)
            #p.ChangeDutyCycle(0)
        time.sleep(length * speed_factor)
        #gpio.set_PWM_dutycycle(pin, 0)
        #p.ChangeDutyCycle(0)
        gpio.hardware_PWM(pin, freq, 000000)
        time.sleep(delta * speed_factor)
    #GPIO.output(led, 0)
    gpio.write(led, 0)
except KeyboardInterrupt:
    pass

#p.stop()
#GPIO.cleanup()
gpio.write(pin, 0)
gpio.write(led, 0)
gpio.set_mode(pin, pigpio.INPUT)
gpio.set_mode(led, pigpio.INPUT)
gpio.stop()
