'''
FastAPI Backend
Must be run as sudo. 
'''
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from accellerator import Pedal
from fastapi.middleware.cors import CORSMiddleware

### Objects
app = FastAPI()
accellerator = Pedal(state='on', location=0)


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
    state: int
    speed: int

class FloatMessage(BaseModel):
    value: float
    
class StringMessage(BaseModel):
    value: str


### General Routes
@app.get('/')
async def root(): 
    return {"Hello its Totus"}

### Accellerator Routes
@app.get('/accellerator/getstate')
def accel_getstate(): 
    print(accellerator.get_state())
    return accellerator.get_state()

@app.get('/accellerator/getlocation')
def accel_getposition(): 
    print(accellerator.get_location())
    accellerator.update_location(1)
    return accellerator.get_location()

@app.put('/accellerator/change_state')
async def accel_turn_on(message: StringMessage):
    if message.value == 'on': 
        accellerator.turn_on()
    elif message.value == 'off': 
        accellerator.turn_off()


@app.put('/accellerator/controller_location')
async def accel_controller_location(message: FloatMessage):
    print("Accellerator Recieved:" , message.value)
    accellerator.update_location(message.value)


# Initialize
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
    
    