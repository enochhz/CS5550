import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

window = tk.Tk()
window.title("Image Processor")
global_width=1000
global_height=800
window.geometry(f"{global_width}x{global_height}")

# Add the main frame, and insert two main frames
main_frame = tk.Frame(window)
main_frame.pack()
image_frame = tk.Frame(main_frame)
tools_frame = tk.Frame(main_frame)
image_frame.pack(side='top')
tools_frame.pack(side='bottom')

# Add two label in the top frame
def display_image(path):
    load = Image.open(path)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img_width, img_height = load.size

def open_image():
    # choose an new image path
    new_image_path =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (
        ("pbm file", "*.pbm"), 
        ("all files","*.*"),
        ("jpeg files","*.jpg")))
    # Display the new image in the frame
    new_image = ImageTk.PhotoImage(Image.open(new_image_path))
    image_label.configure(image=new_image)
    window.update_idletasks()
    return

open_image_button = tk.Button(image_frame, text='Open an image', command=open_image)
open_image_button.pack()
img = ImageTk.PhotoImage(Image.open('./empty_image.png'))
image_label = tk.Label(image_frame, image=img)
image_label.pack()

# Add one label in the bottom frame
tk.Label(tools_frame, text='bottom frame').pack()


window.mainloop()
