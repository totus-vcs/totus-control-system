'''
Stream using a websocket. 
'''
import socket, cv2, pickle, struct, imutils

# Socket Create

class Camera(): 
    def __init__(self, host_ip:str, port:int, cam_index:int): 
        
        self.host_ip = host_ip
        self.port = port
        self.cam_index = cam_index
        
        
        ## CV Stuff
        self.class_names = []
        with open("cv-weights-model/coco_names.txt", "r") as f:
            self.class_names = f.read().strip().split("\n")
            
        # path to the weights and model files
        weights = "cv-weights-model/frozen_inference_graph.pb"
        model = "cv-weights-model/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
        # load the MobileNet SSD model trained  on the COCO dataset
        self.net = cv2.dnn.readNetFromTensorflow(weights, model)
        
    def startSocket(self): 
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host_name = socket.gethostname()
        print('HOST IP:', self.host_ip)
        self.socket_address = (self.host_ip, self.port)

        # Socket Bind
        self.server_socket.bind(self.socket_address)

        # Socket Listen
        self.server_socket.listen(5)
        print("LISTENING AT:", self.socket_address)


        # Socket Accept
        while True:
            client_socket, addr = self.server_socket.accept()
            print('GOT CONNECTION FROM:', addr)
            if client_socket:
                vid = cv2.VideoCapture(self.cam_index)
                
                while (vid.isOpened()):
                    img, frame = vid.read()
                    frame = imutils.resize(frame, width=320)
                    
                    ## Detect Objects here
                    frame = self.detectObjects(frame)
                    
                    a = pickle.dumps(frame) #serialize frame to bytes
                    message = struct.pack("Q", len(a)) + a # pack the serialized data
                    # print(message)
                    try:
                        client_socket.sendall(message) #send message or data frames to client
                    except Exception as e:
                        print(e)
                        self.server_socket.close()
                        vid.release()
                        self.startSocket()
                        
    def detectObjects(self, frame): 
        image = frame
        
        h = image.shape[0]   
        w = image.shape[1]    

        # Create blob from image. 
        blob = cv2.dnn.blobFromImage(
            image, 1.0/127.5, (320, 320), [127.5, 127.5, 127.5])
        # Pass blob through network, get output preduction.
        self.net.setInput(blob)
        output = self.net.forward() # shape: (1, 1, 100, 7)

        CURRENT_ITEMS = []
        
        # loop over the number of detected objects
        for detection in output[0, 0, :, :]: 
            
            # Extract the ID of the detected object to get its name
            class_id = int(detection[1])
            detected_thing = self.class_names[class_id - 1]
            # If it's NOT in list of wanted objects, skip. 
            if detected_thing not in ["person", "bicycle", "car", "motorcycle", "bus", "train", "truck", "traffic light", "street sign", "stop sign", "dog"]: 
                continue
            
            # Confidence of model regarding detected object
            probability = detection[2]
            
            # If confidence under threshold, SKIP
            if probability < 0.5:
                continue

            # perform element-wise multiplication to get
            # the (x, y) coordinates of the bounding box
            box = [int(a * b) for a, b in zip(detection[3:7], [w, h, w, h])]
            box = tuple(box)
            # draw the bounding box of the object
            cv2.rectangle(image, box[:2], box[2:], (0, 255, 0), thickness=2)

            # draw the name of the predicted object along with the probability
            label = f"{self.class_names[class_id - 1].upper()} {probability * 100:.2f}%"
            
            CURRENT_ITEMS.append(self.class_names[class_id - 1].upper())
            
            cv2.putText(image, label, (box[0], box[1] + 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
        return image