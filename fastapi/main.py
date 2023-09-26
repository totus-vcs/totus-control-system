'''
FastAPI Backend
Must be run as sudo. 
'''


from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

from accellerator import Accellerator

### Objects
app = FastAPI()
accel = Accellerator(1, 1)


### Message Classes
# https://fastapi.tiangolo.com/tutorial/body/

class MotorMessage(BaseModel):
    state: bool
    speed: int 


### General Routes
@app.get('/')
async def root(): 
    return {"Hello its Totus"}

### Accellerator Routes
@app.get('/accellerator/getstate')
def accel_getstate(): 
    print(accel.get_state())
    return accel.get_state()

@app.put('/accellerator/turn_on')
async def accel_turn_on(message: MotorMessage):
    if message.state == 1: 
        accel.turn_on()
        
@app.put('/accellerator/turn_off')
async def accel_turn_off(message: MotorMessage):
    if message.state == 0: 
        accel.turn_off()

    


# Initialize
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
    
    