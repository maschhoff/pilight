#!/usr/bin/env python3

# Raspberrypi STX882 Receiver patch
# Run this script on startup
# Requred - pip3 install RPi.GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.IN) # 12 is my gpio pin - enter yours here
