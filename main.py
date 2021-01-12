from tkinter import *           # GUI package
from time import sleep, time
#from keyboard import is_pressed
from pynput.keyboard import Listener
from pynput import mouse
import math
import random

PI_CAMERA = False

#camera function
def get_file_name():  
    return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]+".h264"

IS_PC = True    # debug in pc
if not IS_PC:
    import RPi.GPIO as GPIO

if PI_CAMERA:
    import picamera # pi camera
    cam = picamera.PiCamera()
    fileName = get_file_name()  


STEP =  4                 # SELECT THE STEP 1 to 4
TIME_LED_ON = 0.2         # Time led on 

#default configuration
square_max_iter     = 3   # max number of iterations
max_timer_click     = 5   # max timer to click image
timer_click_mode    = False # set timer mode, False indicate click mode
right_click_mode    = True # if is True, the box change only with right click inside the box (timer_click_mode MUST be False to use this mode)
square_size         = 200 # square width
click_error         = 0   # click error
random_pos          = True #random position    
random_color        = True # square random color picked from color_options
square_color        = [255,0,0] #RGB color if random color is False
colors_options      = [[255,0,0],[255,255,0],[0,0,255]] #option of colors, only work if random_color is True

# STEP 1: RED square 500x500 pixels in the center of screen
if STEP== 1:
    square_max_iter     = 1   # max number of iterations
    max_timer_click     = 5   # max timer to click image
    square_size         = 500 # square width
    click_error         = 0   # click error
    random_pos          = False #random position
    random_color        = False # square random color picked from color_options
    square_color        = [255,0,0] #RGB color if random color is False
    colors_options      = [[255,0,0],[255,255,0],[0,0,255]] #option of colors, only work if random_color is True

# STEP 2: Random color square 500x500 pixels in the center of screen
if STEP== 2:
    square_max_iter     = 1   # max number of iterations
    max_timer_click     = 5   # max timer to click image
    square_size         = 500 # square width
    click_error         = 0   # click error
    random_pos          = False #random position
    random_color        = True # square random color picked from color_options
    square_color        = [255,0,0] #RGB color if random color is False
    colors_options      = [[255,0,0],[255,255,0],[0,0,255]] #option of colors, only work if random_color is True

# STEP 3: Random color square 200x200 pixels in the center of screen
if STEP== 3:
    square_max_iter     = 1   # max number of iterations
    max_timer_click     = 5   # max timer to click image
    square_size         = 200 # square width pixels
    click_error         = 0   # click error
    random_pos          = False #random position
    random_color        = True # square random color picked from color_options
    square_color        = [255,0,0] #RGB color if random color is False
    colors_options      = [[255,0,0],[255,255,0],[0,0,255]] #option of colors, only work if random_color is True

# STEP 4: Random color square 200x200 pixels in the random position of screen
if STEP== 4:
    square_max_iter     = 3   # max number of iterations
    max_timer_click     = 5   # max timer to click image
    square_size         = 200 # square width
    click_error         = 0   # click error
    random_pos          = True #random position    
    random_color        = True # square random color picked from color_options
    square_color        = [255,0,0] #RGB color if random color is False
    colors_options      = [[255,0,0],[255,255,0],[0,0,255]] #option of colors, only work if random_color is True



score = 0   # score used to return right clicks

# variables to control program
square_show = False  #indicates if the square is on screen
square_timer = 0     #used to control time
square_iter = 0      #used to count program iterations
square_pos_x = None     #stores x square's position
square_pos_y = None     #stores y square's coordenate
clicked = False         #indicates if left click is pressed
isRunning = True        #indicates if program is running
changeRightClick = False #indicate right click inside box


canvas = None      #used to support square un tkinter

#Configure GPIO control  
SUCCESS_LED = 17
FAIL_LED =27

#Function that indicates if the box was pressed or not. The time of the led on
# is added to the time between the appearence of squares.
def turn_on_led(status):
    if not IS_PC:
        GPIO.setmode(GPIO.BCM) #set mode to GPIO control
        GPIO.setup(SUCCESS_LED, GPIO.OUT) # set GPIO 17 as output SUCCESS LED
        GPIO.setup(FAIL_LED, GPIO.OUT) # set GPIO 27 as output FAIL LED

        if status == "SUCCESS":
            GPIO.output(SUCCESS_LED, True) ## turn on SUCCESS LED
            sleep(TIME_LED_ON)
            GPIO.output(SUCCESS_LED, False) ## turn off SUCCESS LED

        elif status == "FAIL":
            GPIO.output(FAIL_LED, True) ## Enciendo FAIL LED
            sleep(TIME_LED_ON)
            GPIO.output(FAIL_LED, False) ## turn off FAIL LED
        GPIO.cleanup() # clear GPIOs

def led_success():
    turn_on_led("SUCCESS")

def led_failed():
    turn_on_led("FAIL")

#Function that is executed every time the mouse is clicked
#and get the position x,y of the cursor.
def on_click(x, y, button, pressed):
    global square_show, clicked, score, square_pos_x, square_pos_y, square_size, changeRightClick

    #print("margins x:{}-{}  y:{}-{}".format(square_pos_x, square_pos_x+square_size, square_pos_y, square_pos_y+square_size)) #debug

    if button == mouse.Button.left and pressed==True:       #check if left button is clicked, pressed=Trye indicates pressed, False indicates release
        print("Click position: {},{}".format(x,y))              #debug: show cursor position on console
        if x>= square_pos_x-click_error and x<= square_pos_x+square_size+click_error and y>= square_pos_y-click_error and y<= square_pos_y+square_size+click_error : #check if click is inside square+error area.
            score=score+1                                   #add 1 to score if is a right click, inside a square+error area.
            print(">> CLICK INSIDE TARGET!")
            led_success()
            changeRightClick=True
        else:
            print(">> CLICK FAILED!")
            led_failed()
        clicked = True

    if button == mouse.Button.right and pressed ==True: #check if right click is pressed
        print("Right click: {},{}".format(x,y))


'''
CREATE GUI
'''

#start camera video
if PI_CAMERA:
    fileName = get_file_name()  
    cam.start_recording(fileName)  

window = Tk()   #init Tkinter window
window.title("Click Tracker v0.1")

mouse_listener = mouse.Listener(on_click=on_click)     #sets mouse listener passing function prior defined
mouse_listener.start()                                 #starts mouse listener

ws = window.winfo_screenwidth() #gets the width of screen
hs = window.winfo_screenheight() #gets the heigth of screen
print("[!] SCREEN SIZE {}x{}".format(ws,hs))
w_ws = ws
w_hs = hs
#w_ws = math.ceil(ws/2) #reduce width ,scale
#w_hs = math.ceil(hs/2) #reduce height, scale
window.attributes("-fullscreen", True)
window.configure(background='black')
window.geometry("{}x{}+{}+{}".format(w_ws,w_hs,-10,-5)) #sets size of windows

# Function to create squares on screen, receive canvas as input
def createSquare(c):
    global square_show, square_timer, square_iter, isRunning, square_max_iter
    global square_pos_x, square_pos_y, random_pos, random_color
    
    if square_show == False: # checks if square is on screen, if not, create it
        if random_pos:
            square_pos_x = random.randint(0+square_size,w_ws-square_size) #random x position on screen
            square_pos_y = random.randint(0+square_size,w_hs-square_size) #random y position on screen
        else:
            square_pos_x = (w_ws-square_size)/2
            square_pos_y = (w_hs-square_size)/2
        if random_color:
            rcol = random.choice(colors_options)
        else:    
            rcol =  square_color
        colorval = "#%02x%02x%02x" % (rcol[0], rcol[1], rcol[2]) # rgb to hexadecimal format
        c.create_rectangle(square_pos_x, square_pos_y, square_pos_x+square_size, square_pos_y+square_size, fill=colorval) #create blue square
        square_show = True   # set true to indicates that square is on screen
        square_iter = square_iter + 1 # add 1 to program iteration
        square_timer = time()    # restart timer


canvas = Canvas(window, width=w_ws, height=w_hs) #create canvas with screen size
canvas.configure(background='black')    #set background color
canvas.pack()      #add canvas to window screen

#loop of program
while True:    
    if square_iter>square_max_iter:   #checks if program reach max iterations
        break

    if square_show == False: #checks if square is on screen, if not, create one
        if square_iter >= square_max_iter:
            break
        print("--------------------------------------\n[+] Square {} created!".format(square_iter))
        createSquare(canvas) #create square
        print("Square position: {},{}".format(square_pos_x,square_pos_y))
    
    if timer_click_mode:
        if time()- square_timer > max_timer_click or clicked: # checks time of square on screen or left button of mouse was clicked
            canvas.delete("all")    #delete all objects in canvas
            square_show = False  #set false to create a new square
            clicked = False         #set false to init click state
            square_timer = time()    #restart timer
    elif clicked:
        if changeRightClick and right_click_mode:
            canvas.delete("all")    #delete all objects in canvas
            square_show = False  #set false to create a new square
            clicked = False         #set false to init click state
            square_timer = time()    #restart timer
            changeRightClick = False
        elif not right_click_mode:
            canvas.delete("all")    #delete all objects in canvas
            square_show = False  #set false to create a new square
            clicked = False         #set false to init click state
            square_timer = time()    #restart timer
    

    
    
    if isRunning == False:  #end program
        break
    
    sleep(0.1)

    

    window.update() #function mandatory to update tkinter gui

mouse_listener.stop()   #stop listener when program was ended
window.destroy()        #destroy windows of tkinter

#finish camera video
if PI_CAMERA:
    cam.stop_preview()
    cam.stop_recording()
print("--------------------------------------\n[!] YOUR SCORE IS {} OF {}".format(score, square_max_iter))
print("--------------------------------------\n")
