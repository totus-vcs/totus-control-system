from adafruit_servokit import ServoKit
import board
import busio


class Motor: 
    
    def __init__(self, 
                 name, 
                 state, 
                 min_angle_location, 
                 max_angle_location,
                 zero_angle_location,
                 busNum): 
        
        ## Inputs ##
        self.name = name # Name, just for printing/debugging
        self.state = state # On and Off
        self.min_angle_location = min_angle_location # Where does the motor sit when it is '0' off
        self.max_angle_location = max_angle_location
        self.zero_angle_location = zero_angle_location
        self.angle_location = zero_angle_location # Current angle motor is
        self.busNum = busNum # Location on the I2C Chip (0, 1, 2, 3 etc)

        ## Setting up the bus ## 
        print("Start Initializing Motor:", self.name)
        self.bus = (busio.I2C(board.SCL_1, board.SDA_1)) # i2c_bus0
        self.kit = ServoKit(channels=16, i2c=self.bus)
        print("Finished Initializing Motor:", self.name)
        
        
    ### Get Definitions ###
    def get_state(self): 
        return self.state
    
    def get_angle_location(self): 
        return self.angle_location
    
    ### Turn on and Off ###
    def turn_on(self): 
        self.return_to_zero()
        self.state = 'on'
        return self.state
    
    def turn_off(self): 
        self.return_to_zero()
        self.state = 'off'
        return self.state
    
    ### Move Motors ###
    def return_to_zero(self): 
        self.angle_location = self.zero_angle_location
        self.kit.servo[self.busNum].angle = self.angle_location
        return self.angle_location
    
    def move_to_angle(self, input_location): 
        if self.state == "on":
            self.angle_location = self.calculate_angle(input_location)
            self.kit.servo[self.busNum].angle = self.angle_location
            print(self.name, "Moving to", self.angle_location)
        if self.state == "off":
            print(self.name, "Move to Angle Failed - Motor is OFF")
        return self.angle_location
    
    def calculate_angle(self, input_location): 
        range = self.max_angle_location - self.min_angle_location
        
        if range == 0: 
            # This is a problem. Motor will not move
            print(self.name, "Motor Error - inncorect range specified")
            return None

        if range > 0: 
            # Default easy to deal with state
            # E.g. min = 20, max = 40
            output = input_location * range + self.min_angle_location
            return output
            
        if range < 0:
            # Range is Negative
            # By default, servokit actuation range is 180 degrees 
            # https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/using-the-adafruit-library
                # Sidenote, motors might not actually move "180" degrees
            # Therefore, e.g. min is 170, max is 10
            # I.e. moving through zero
            range = (180 - self.max_angle_location) + self.min_angle_location
            output = input_location * range + self.min_angle_location
            if output > 180: 
                output = output - 180
            return output
            