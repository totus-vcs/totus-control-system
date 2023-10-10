from adafruit_servokit import ServoKit
import board
import busio
import time
import socket, cv2, pickle, struct, imutils
import asyncio

class Camera: 
    
    def __init__(self, state): 
        self.state = state

    # Get State    
    def get_state(self):
        return self.state
    
    def turn_on(self): 
        self.state = 'on'
        return self.state
    
    # Turn Off
    def turn_off(self): 
        self.state = 'off'
        return self.state
    
