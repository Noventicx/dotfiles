#!/usr/bin/env python3

from __future__ import print_function
from random import randrange

import os
import sys
import random
import pywal
import ast
import phue
import argparse
from rgbxy import Converter, GamutC
from configparser import ConfigParser

import argparse

argparser=argparse.ArgumentParser()
argparser.add_argument('-i', '--ip', action="store", dest='ip', help="provide bridge-ip (1.1.1.1)")
argparser.add_argument('-c', '--config', action="store", dest="config", help="provide config (/path/to/file)") 
argparser.add_argument('-cl', '--color', action="store", dest="color", help="provide one single color for each lightin hex (ffffff)")
argparser.add_argument('-ca', '--color-all', action="store", dest="colorall", help="provide colors for each lights in hex ('ffffff,fffff')")
argparser.add_argument('-ccl', '--config-color', action="store_true", dest="configcolor", help="use colors from config")
argparser.add_argument('-rb', '--random-brightness', action='store_true', dest="randombrightness", help="use random brightness for each light")
argparser.add_argument('-b', '--brightness', action="store", dest="brightness", type=int, help="provide one brightnessvalue for the lights 1-254 (1)")
argparser.add_argument('-bl', '--brightness-light', action="store", dest="brightnesslight", help="provide brighnessvalues for each light 1-254 ('1,1')")
argparser.add_argument('-l', '--lights', action='store', dest="lights", help="specify the light/lights to use ('light1,light2')")

args = argparser.parse_args()
iparg = args.ip
configarg = args.config
colorarg = args.color
colorallarg = args.colorall
configcolorarg = args.configcolor   
brightnessarg = args.brightness
brightnesslightarg = args.brightnesslight
randombrightnessargs = args.randombrightness
lightsarg = args.lights

br=0

home = os.environ['HOME']
filepath = home + '/.config/hue-wal/config'

if configarg:
    filepath = configarg
    
config = ConfigParser()

try:
    config.read(os.path.join(os.path.dirname(__file__), filepath))

    BRIDGE_IP = config['bridge']['ip']
    LIGHTS = ast.literal_eval(config['lights']['name'])
    BRIGHTNESS = ast.literal_eval(config['lights']['brightness'])
    try:
        COLORS = ast.literal_eval(config['lights']['colors'])
    except:
        print()
except:                                                                                                                                          
    print(                                                                                                                                       
        'No configfile',
        'in',                             
        filepath,
        file=sys.stderr,                                                                                                                         
    )                                                                                                                                            
def Convert(string):
    li = list(string.split(","))
    return li

def Convert_Color(string):
    li = list(string.split(","))
    return li[br]

def Convert_to_int(string):
    li = list(string.split(","))
    for i in range(0, len(li)):
        li[i] = int(li[i])
    return li[br]

if lightsarg:
    LIGHTS = Convert(lightsarg)

if iparg:    
    BRIDGE_IP = iparg    

converter = Converter(GamutC)

#wal colors
def magic(s):

    s = s.lstrip("#")
    return tuple(int(s[i:i+2], 16) for i in (0, 2 ,4))
wal_colors = list(map(magic, list(pywal.colors.get(pywal.wallpaper.get(), 4)["colors"].values())))

# Helper funciton to generate interesting colors
def random_color():
    color = random.choice(wal_colors)
    colortohex = '%02x%02x%02x' % color
    colorxy = converter.hex_to_xy(colortohex)
    color = colorxy
    
    if colorarg:
        color = converter.hex_to_xy(colorarg)
    
    if colorallarg:
        color = converter.hex_to_xy(Convert_Color(colorallarg))

    if configcolorarg:
        try:
            color = converter.hex_to_xy(COLORS[br])
        except:
            print("no COLORS given in config using random colors")
    return color

def random_bri():
    if randombrightnessargs:
        bri = randrange(254)
    elif brightnessarg:
        bri = brightnessarg
    elif brightnesslightarg:
        bri = Convert_to_int(brightnesslightarg)
    else:
        try:
            bri = BRIGHTNESS[br]
        except:
            print("no BRIGHTNESS given in config using random BRIGHTNESS")
            bri = randrange(254)

    return bri

try:                                                                                                                                             
    bridge = phue.Bridge(BRIDGE_IP)                                                                                                 
except:                                                                                                                                          
    print(                                                                                                                                       
        'Cannot connect to Hue Bridge. Provide correct IP address',                                                                              
        file=sys.stderr,                                                                                                                         
    )                                                                                                                                            
    sys.exit(1)                                                                                                                                  
bridge.connect()

c = 0
for light in LIGHTS:                                                                                                      
                        
    state = {                                                                                                                  
        'xy': random_color(),                                                                                                                                 
        'bri': random_bri()                                                                                                                           
    }                    
    c = c+1
    br = br+1
    print (light, state)    
    bridge.set_light(light, state)    
