import time
import picamera
import datetime  

def get_file_name():  
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]+".h264"


cam = picamera.PiCamera()

fileName = get_file_name()  
cam.start_preview()
cam.start_recording(fileName)  
time.sleep(10)
cam.stop_preview()
cam.stop_recording()