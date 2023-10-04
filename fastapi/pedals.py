from adafruit_servokit import ServoKit
import board
import busio
import time
from time import sleep


class Pedal: 
    
    def __init__(self, state, location, busNum): 
        self.state = state
        self.location = location
        self.busNum = int(busNum)
        
        # On the Jetson Nano
        # Bus 0 (pins 28,27) is board SCL_1, SDA_1 in the jetson board definition file
        # Bus 1 (pins 5, 3) is board SCL, SDA in the jetson definition file
        # Default is to Bus 1; We are using Bus 0, so we need to construct the busio first ...
        print("Initializing Accellerator Servos")
        self.bus = i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
        
        # kit[0] is the bottom servo
        # kit[1] is the top servo
        print("Initializing Accellerator ServoKit")
        self.kit = ServoKit(channels=16, i2c=i2c_bus0)
        
        print("Finished Initialzing Pedal")

    # Get State    
    def get_state(self):
        return self.state
    
    # Get Location
    def get_location(self): 
        return self.location

    # Turn On 
    def turn_on(self): 
        self.return_to_zero()
        self.state = 'on'
        return self.state
    
    # Turn Off
    def turn_off(self): 
        self.return_to_zero()
        self.state = 'off'
        return self.state
    
    # Test
    def test_1(self): 
        if self.state == 'on': 
            print("Motor Test Sweep")
            sweep = range(0,1)
            for degree in sweep :
                self.kit.servo[self.busNum].angle=degree
                # kit.servo[1].angle=degree
                time.sleep(0.01)

            time.sleep(0.1)

            sweep = range(180,0, -1)
            for degree in sweep :
                self.kit.servo[self.busNum].angle=degree
    
    # Test 2            
    def test_2(self): 
        if self.state == 'on': 
            print("testmessage")
            self.kit.servo[self.busNum].angle=2
    
    def convert_controller_to_servo(self, controller_location):
        return round(controller_location * (20))
    
    # Update Servo Location
    def update_location(self, final_location):
        if self.state == 'on': 
            
            final_location = self.convert_controller_to_servo(final_location)
            
            # if final_location < self.location: 
            #     self.location = self.location - 1 
            # if final_location > self.location: 
            #     self.location = self.location + 1 
            
            # print("Final Loc:", final_location, "Current Loc:", self.location)
            
            self.kit.servo[self.busNum].angle = self.location
        
        self.location = final_location
        return self.location 
    
    def return_to_zero(self): 
        self.kit.servo[self.busNum].angle = 0
