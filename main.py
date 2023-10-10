from multiprocessing import Process

import uvicorn
import camera

# IP = "10.0.0.202"          
IP = "192.168.195.54"

front_camera = camera.Camera(IP, 8152, 0)
left_camera = camera.Camera(IP, 8160, 1)
# right_camera = camera.Camera("10.0.0.202", 8170, 2)

def countdown(n): 
    print("Test process Start")
    while n > 0:
        n = n - 1
    print("Test process Stop")

if __name__=="__main__":
    
    p2 = Process(target = uvicorn.run, args=["motorapi:app"], kwargs={'host': IP, 'port': 5000, 'reload':True})
    
    p3 = Process(target = front_camera.startSocket)
    p4 = Process(target = left_camera.startSocket)
    # p5 = Process(target = right_camera.startSocket)
    
    
    p2.start()
    p3.start()
    p4.start()
    # p5.start()
    
    p2.join()
    p3.join()
    p4.join()
    # p5.join()