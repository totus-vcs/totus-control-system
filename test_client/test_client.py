import requests

url = 'http://10.0.0.202/accellerator/turn_off'
myobj = {"state": 0, "speed": 0}

x = requests.put(url, json = myobj)



# message = MotorMessage({"state": 0, "speed": 0})

# print(message)