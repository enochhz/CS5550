from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

global_width, global_height = 800, 800

class Window(Frame):

    # top frames
    image_frame = ""
    tools_frame = ""
    # items for image frame
    open_image_button = ""
    image_label = ""
    img = ""
    # items for tools frame 
    tools_label = ""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.add_main_frames()

    def add_main_frames(self):
        self.image_frame = Frame(self)
        self.image_frame.pack(side='top')
        self.configure_image_frame()
        self.tools_frame = Frame(self)
        self.tools_frame.pack(side='bottom')
        self.configure_tools_frame()
    
    def configure_image_frame(self):
        self.open_image_button = Button(self.image_frame, width=20, height=2, text='Open an image', command=self.open_image)
        self.open_image_button.pack()
        # update the initial image
        self.img = ImageTk.PhotoImage(Image.open('./empty_image.png'))
        self.image_label = Label(self.image_frame, image=self.img)
        self.image_label.pack()

    def open_image(self):
        # choose an new image path
        new_image_path =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (
            ("pbm file", "*.pbm"), 
            ("all files","*.*"),
            ("jpeg files","*.jpg")))
        # Display the new image in the frame
        self.img = ImageTk.PhotoImage(Image.open(new_image_path))
        self.image_label.configure(image=self.img)

    def configure_tools_frame(self):
        self.tools_label = Label(self.tools_frame, text='Tools')
        self.tools_label.pack()

def main():
    root = Tk()
    app = Window(root)
    root.wm_title("Image Processor")
    # root.geometry(f"{global_width}x{global_height}")
    root.mainloop()

if __name__ == '__main__':
    main()
