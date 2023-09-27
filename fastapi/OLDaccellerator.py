from adafruit_servokit import ServoKit
import board
import busio
import time

class Accellerator: 
    
    def __init__(self, state: bool, speed: float): 
        self.state = state
        self.speed = speed
        
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
        
        print("Finished Initialzing Accellerator")

        
    def get_state(self):
        return self.state
    
    def get_speed(self): 
        return self.speed
    
    def turn_on(self): 
        self.state = 1
        print("Accellerator_On")
        return self.state
    
    def turn_off(self): 
        self.state = 0
        return self.state
    
    def test(self): 
        if self.state: 
            print("testmessage")
            sweep = range(0,180)
            for degree in sweep :
                self.kit.servo[0].angle=degree
                # kit.servo[1].angle=degree
                time.sleep(0.01)

            time.sleep(0.5)

            sweep = range(180,0, -1)
            for degree in sweep :
                self.kit.servo[0].angle=degree
    
    def controller_location_to_pedal_degree(self, controller_location): 
        if self.state: 
            pass # TODO (convert value of pedal to degree?)
                
    def move_to_location(self): 
        if self.state: 
            pass # TODO (delete pass)


accel = Accellerator(1, 1)

accel.turn_on()