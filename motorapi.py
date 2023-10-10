from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from motors import Motor 

### Objects ###
app = FastAPI()
brake = Motor(name='brake', 
              state='on', 
              min_angle_location=0, 
              max_angle_location=90, 
              zero_angle_location=45, 
              busNum=0)
accellerator = Motor(name='accellerator', 
              state='on', 
              min_angle_location=0, 
              max_angle_location=90, 
              zero_angle_location=45, 
              busNum=1)
steering = Motor(name='steering', 
              state='on', 
              min_angle_location=0, 
              max_angle_location=90, 
              zero_angle_location=45, 
              busNum=2)


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

class FloatMessage(BaseModel):
    value: float
    
class StringMessage(BaseModel):
    value: str


### General Routes ###
@app.get('/')
def root(): 
    return "Welcome to Totus"
 

### Get State ### 
@app.get('/brake/state')
def get_state_brake(): 
    return brake.state

@app.get('/accellerator/state')
def get_state_accellerator(): 
    return accellerator.state

@app.get('/steering/state')
def get_state_steering(): 
    return steering.state



### Get angle_location ### 
@app.get('/brake/angle_location')
def get_angle_location_brake(): 
    return brake.angle_location

@app.get('/accellerator/angle_location')
def get_angle_location_accellerator(): 
    return accellerator.angle_location

@app.get('/steering/angle_location')
def get_angle_location_steering(): 
    return steering.angle_location



### Change State ###
@app.put('/brake/change_state')
def brake_turn_on(message: StringMessage):
    if message.value == 'on': 
        brake.turn_on()
    elif message.value == 'off': 
        brake.turn_off()
        
@app.put('/accellerator/change_state')
def accellerator_turn_on(message: StringMessage):
    if message.value == 'on': 
        accellerator.turn_on()
    elif message.value == 'off': 
        accellerator.turn_off()

@app.put('/steering/change_state')
def steering_turn_on(message: StringMessage):
    if message.value == 'on': 
        steering.turn_on()
    elif message.value == 'off': 
        steering.turn_off()
        
        
## Update Servo Locations ### 
@app.put('/accellerator/controller_location')
async def accellerator_controller_location(message: FloatMessage):
    print("Accellerator Recieved:" , message.value)
    accellerator.move_to_angle(message.value)

@app.put('/brake/controller_location')
async def brake_controller_location(message: FloatMessage):
    print("Brake Recieved:" , message.value)
    brake.move_to_angle(message.value)

@app.put('/steering/controller_location')
async def steering_controller_location(message: FloatMessage):
    print("Steering Recieved:" , message.value)
    steering.move_to_angle(message.value)