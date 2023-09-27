'''
FastAPI Backend
Must be run as sudo. 
'''


from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from accellerator import Accellerator
from fastapi.middleware.cors import CORSMiddleware

### Objects
app = FastAPI()
a_pedal = Accellerator(state=1, location=0)


# Add CORS Middleware
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


### Message Classes
# https://fastapi.tiangolo.com/tutorial/body/

class MotorMessage(BaseModel):
    state: bool
    speed: int

class FloatMessage(BaseModel):
    value: float


### General Routes
@app.get('/')
async def root(): 
    return {"Hello its Totus"}

### Accellerator Routes
@app.get('/accellerator/getstate')
def accel_getstate(): 
    print(a_pedal.get_state())
    return a_pedal.get_state()

@app.get('/accellerator/getlocation')
def accel_getposition(): 
    print(a_pedal.get_location())
    a_pedal.update_location(1)
    return a_pedal.get_location()

@app.put('/accellerator/turn_on')
async def accel_turn_on(message: MotorMessage):
    if message.state == 1: 
        a_pedal.turn_on()
        
@app.put('/accellerator/turn_off')
async def accel_turn_off(message: MotorMessage):
    print(message.state)
    print(message.speed)
    if message.state == None: 
        pass
    elif message.state == 0: 
        a_pedal.turn_off()

@app.put('/accellerator/controller_location')
async def accel_controller_location(message: FloatMessage):
    print("Accellerator Recieved:" , message.value)
    a_pedal.update_location(message.value)


# Initialize
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
    
    