import tkinter
import PIL.Image, PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
import time


SET_WIDTH = 650  # Window width
SET_HEIGHT = 370  # Window height

# Load Video Stream
stream = cv2.VideoCapture(r"C:\Users\User\Desktop\DRS Review System\clip.mp4")

# Get video properties
video_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculate scale to fit video inside SET_WIDTH & SET_HEIGHT while keeping aspect ratio
scale_width = SET_WIDTH / video_width
scale_height = SET_HEIGHT / video_height
scale = min(scale_width, scale_height)  # Maintain aspect ratio


def play(speed):
    print(f"You clicked on play. Speed is {speed}")

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        return

    # Resize while maintaining aspect ratio
    frame = imutils.resize(frame, width=int(video_width * scale), height=int(video_height * scale))

    # Convert to ImageTk format
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    # Clear canvas and set black background before updating frame
    canvas.delete("all")
    canvas.configure(bg="black")
    canvas.create_image(SET_WIDTH//2, SET_HEIGHT//2, image=frame, anchor=tkinter.CENTER)
    canvas.image = frame  # Keep a reference
    canvas.create_text(130, 25, fill="green", font="Times 20 bold", text="Decision Pending...")



def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")


def pending(decision):
    image_path = r"C:\Users\User\Desktop\DRS Review System\pending.png"
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    # Clear canvas before updating frame
    canvas.delete("all")
    canvas.create_image(SET_WIDTH//2, SET_HEIGHT//2, image=frame, anchor=tkinter.CENTER)
    canvas.image = frame
    window.update()

    time.sleep(1.5)

    decisionImg = r"C:\Users\User\Desktop\DRS Review System\out.png" if decision == "out" else r"C:\Users\User\Desktop\DRS Review System\not_out.png"
    frame = cv2.imread(decisionImg)

    if frame is None:
        print(f"Error: Unable to load image at {decisionImg}")
        return

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

    # Clear canvas before updating frame
    canvas.delete("all")
    canvas.create_image(SET_WIDTH//2, SET_HEIGHT//2, image=frame, anchor=tkinter.CENTER)
    canvas.image = frame
    window.update()


def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")


# Create GUI Window
window = tkinter.Tk()
window.title("UDRS")

canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT, bg="black")  # Black background
canvas.pack()

# Load and display welcome image
welcome_path = r"C:\Users\User\Desktop\DRS Review System\welcome.jpeg"
welcome_img = cv2.imread(welcome_path)

if welcome_img is not None:
    welcome_img = cv2.cvtColor(welcome_img, cv2.COLOR_BGR2RGB)
    welcome_img = imutils.resize(welcome_img, width=SET_WIDTH, height=SET_HEIGHT)
    welcome_img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(welcome_img))
    canvas.create_image(SET_WIDTH//2, SET_HEIGHT//2, image=welcome_img, anchor=tkinter.CENTER)
    canvas.image = welcome_img  # Keep reference
else:
    print(f"Error: Unable to load image at {welcome_path}")

# Control Buttons
btn = tkinter.Button(window, text="<< Previous (Fast)", width=50, command=partial(play, -20))
btn.pack()

btn = tkinter.Button(window, text="<< Previous (Slow)", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Next (Fast) >>", width=50, command=partial(play, 20))
btn.pack()

btn = tkinter.Button(window, text="Next (Slow) >>", width=50, command=partial(play, 2))
btn.pack()

btn = tkinter.Button(window, text="Give Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give Not Out", width=50, command=not_out)
btn.pack()

window.mainloop()
