from adafruit_servokit import ServoKit
import board
import busio
import time

print("Start Init")
bus = i2c_bus0 = (busio.I2C(board.SCL_1, board.SDA_1))
kit = ServoKit(channels=16, i2c=i2c_bus0)
print("Finished Init")
 
degree = 180
print(degree)
kit.servo[0].angle=degree
time.sleep(10)

degree = 0
print(degree)
kit.servo[0].angle=degree
time.sleep(10)
    
degree = 45
print(degree)
kit.servo[0].angle=degree
time.sleep(5)

degree = 0
print(degree)
kit.servo[0].angle=degree
time.sleep(5)

degree = 90
print(degree)
kit.servo[0].angle=degree
time.sleep(5)

degree = 0
print(degree)
kit.servo[0].angle=degree
time.sleep(5)



# accel = Accellerator(1, 1)
# accel.test_NEW()