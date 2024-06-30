
"""
import tkinter                          # For creating GUI elements like windows, canvases, and buttons
import cv2                              # For reading and processing video and image files  OpenCV:-(Open Source Computer Vision Library)
import PIL.Image, PIL.ImageTk           # For converting images for display in Tkinter
from functools import partial           # For creating partial functions for button commands
import threading                        # For running functions in separate threads to keep the GUI responsive
import imutils                          # For convenient image processing functions like resizing
import time                             # For adding delays between displaying images

"""



import tkinter
import cv2                          # pip install opencv-python
import PIL.Image, PIL.ImageTk       # pip install pillow
from functools import partial       # included in the Python standard library
import threading
import imutils                      # pip install imutils
import time


## take input
video_clip = input("enter the video file \n")

# Initialize global variables
stream = cv2.VideoCapture(video_clip)
flag = True

# Function to play video at a given speed
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    # Set the frame position
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    
    # Resize and convert the frame
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    
    # Update the canvas image
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    
    # Display "Decision Pending" text on the first click
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag

# Function to handle pending decision
def pending(decision):
    # Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    
    # Wait for a few seconds
    time.sleep(3)
    
    # Display sponsor image
    frame = cv2.cvtColor(cv2.imread("sponser.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    
    # Wait for a few seconds
    time.sleep(3)
    
    # Display the decision image
    decisionImg = "out.png" if decision == 'out' else "notout1.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

# Function to handle "Out" decision
def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

# Function to handle "Not Out" decision
def notout():
    thread = threading.Thread(target=pending, args=("notout",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Set the dimensions of the screen
SET_WIDTH = 650
SET_HEIGHT = 360

# Initialize the Tkinter GUI
window = tkinter.Tk()
window.title("Third Umpire Review System")

# Load and display the initial image
cv_img = cv2.cvtColor(cv2.imread("DRS.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
img_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -20))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text=" Next (fast) >>", width=50, command=partial(play, 20))
btn.pack()

btn = tkinter.Button(window, text=" Next (slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=notout)
btn.pack()

window.mainloop()
