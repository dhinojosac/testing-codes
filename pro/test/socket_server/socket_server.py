import socket
import time 
from  threading import *

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 8765

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print("[!] Server listening on {} and port {}".format(host , port))
s.listen(1)
conn, addr = s.accept()
print('[+] Connected by {}'.format(addr))

while True:

    try:
        data = conn.recv(1024)

        if not data: break
        print("[+] Client sent:{}".format( data.decode() ))

        if "START" in data.decode():
            print("[!] Client has started the program")
            conn.sendall(b'OK')
        elif "BYE" in data.decode():
            print("[!] Client has finished the program")
            conn.close()
        else:
            conn.sendall(b'KO')

    except socket.error:
        print("Error Occured.")
        break

print("[!] Server will be shut down")
conn.close()