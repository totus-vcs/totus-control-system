'''
Camera Stream using Websocket
'''

import socket, cv2, pickle, struct, imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = '10.0.0.202'
print('HOST IP:', host_ip)
port = 8123
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    
    if client_socket:
        try: 
            vid = cv2.VideoCapture(1)
        except: 
            continue 
        while (vid.isOpened()):
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame) #serialize frame to bytes
            message = struct.pack("Q", len(a)) + a # pack the serialized data
            
            try:
                client_socket.sendall(message) #send message or data frames to client
            except Exception as e:
                print(e)
                vid.release()
                # raise Exception(e)
                break

