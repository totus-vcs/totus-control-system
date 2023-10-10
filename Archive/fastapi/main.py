'''
FastAPI Backend
Must be run as sudo. 
'''
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from pedals import Pedal
from steering import Steering
from camera import Camera
from fastapi.middleware.cors import CORSMiddleware

### Objects ###
app = FastAPI()
print(" --> Creating Accellerator <--- ")
accellerator = Pedal(state='on', location=0, busNum=0)
print(" --> Creating Pedal <--- ")
brake = Pedal(state='on', location=0, busNum=1)
print(" --> Creating Steering <--- ")
steer = Steering(state='on', location=0, busNum=2)
print(" --> Creating FrontCam <--- ")
frontcam = Camera(state='off')
print(" --> Creating LeftCam <--- ")
leftcam = Camera(state='off')
print(" --> Creating RightCam <--- ")
rightcam = Camera(state='off')



### Add CORS Middleware ###
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### Message Classes ###
# https://fastapi.tiangolo.com/tutorial/body/

class MotorMessage(BaseModel):
    state: int
    speed: int

class FloatMessage(BaseModel):
    value: float
    
class StringMessage(BaseModel):
    value: str


### General Routes ###

@app.get('/')
async def root(): 
    return "Welcome to Totus"

### Get State ###

@app.get('/accellerator/getstate')
def accel_getstate(): 
    print(accellerator.get_state())
    return accellerator.get_state()

@app.get('/brake/getstate')
def brake_getstate(): 
    print(brake.get_state())
    return brake.get_state()

@app.get('/steering/getstate')
def steer_getstate(): 
    print(steer.get_state())
    return steer.get_state()

@app.get('/frontcam/getstate')
def frontcam_getstate(): 
    print(frontcam.get_state())
    return frontcam.get_state()

@app.get('/leftcam/getstate')
def leftcam_getstate(): 
    print(leftcam.get_state())
    return leftcam.get_state()

@app.get('/rightcam/getstate')
def rightcam_getstate(): 
    print(rightcam.get_state())
    return rightcam.get_state()

### Get Location ###

@app.get('/accellerator/getlocation')
def accel_getposition(): 
    print(accellerator.get_location())
    return accellerator.get_location()

@app.get('/brake/getlocation')
def brake_getposition(): 
    print(brake.get_location())
    return brake.get_location()

@app.get('/steering/getlocation')
def steer_getposition(): 
    print(steer.get_location())
    return steer.get_location()

### Change State ###

@app.put('/accellerator/change_state')
async def accel_turn_on(message: StringMessage):
    if message.value == 'on': 
        accellerator.turn_on()
    elif message.value == 'off': 
        accellerator.turn_off()
        
@app.put('/brake/change_state')
async def brake_turn_on(message: StringMessage):
    if message.value == 'on': 
        brake.turn_on()
    elif message.value == 'off': 
        brake.turn_off()

@app.put('/steering/change_state')
async def steer_turn_on(message: StringMessage):
    if message.value == 'on': 
        steer.turn_on()
    elif message.value == 'off': 
        steer.turn_off()
        
@app.put('/frontcam/change_state')
async def frontcam_turn_on(message: StringMessage):
    if message.value == 'on': 
        frontcam.turn_on()
    elif message.value == 'off': 
        frontcam.turn_off()
        
@app.put('/leftcam/change_state')
async def leftcam_turn_on(message: StringMessage):
    if message.value == 'on': 
        leftcam.turn_on()
    elif message.value == 'off': 
        leftcam.turn_off()
        
@app.put('/rightcam/change_state')
async def rightcam_turn_on(message: StringMessage):
    if message.value == 'on': 
        rightcam.turn_on()
    elif message.value == 'off': 
        rightcam.turn_off()
    
### Update Servo Location ###

@app.put('/accellerator/controller_location')
async def accel_controller_location(message: FloatMessage):
    print("Accellerator Recieved:" , message.value)
    accellerator.update_location(message.value)

@app.put('/brake/controller_location')
async def brake_controller_location(message: FloatMessage):
    print("Brake Recieved:" , message.value)
    brake.update_location(message.value)

@app.put('/steering/controller_location')
async def steer_controller_location(message: FloatMessage):
    print("Steering Recieved:" , message.value)
    steer.update_location(message.value)

    
    
### Initialize ###
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
    
    
    