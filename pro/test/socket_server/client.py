import socket
import datetime
import time

counter = 0

def get_time():
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

host = "127.0.0.1"
port = 8765

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

s.sendall("START AT {}".format(get_time()).encode()) #Send init command

while True:

    if counter >= 10:
        s.sendall("FINISH AT {}".format(get_time()).encode()) #Send finish command
        time.sleep(1)
        break
    s.sendall( "{}".format(counter).encode() ) # send ticks

    data =  s.recv(1024)
    if not data: pass
    else:
        print("Server sent: ", data.decode())
    time.sleep(1)
    counter+=1 #add counter

s.close()
