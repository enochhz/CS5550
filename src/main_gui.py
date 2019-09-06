from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

global_width, global_height = 800, 1000

class Window(Frame):

    # top frames
    header_frame, image_frame, tools_frame = "", "", ""

    # header frame items
    open_image_button = ""

    # image frame items
    image_label, img_path, img, img_info = "", "./empty_image.png", "", ""

    # tools frame items
    resize_frame = ""
    width_input, height_input, resize_button = "", "", ""

    zoom_shrink_frame = ""
    zoom_shrink_scale = ""

    gray_level_frame = ""
    gray_level_input, gray_level_button = "", ""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.add_main_frames()

    def add_main_frames(self):
        self.header_frame = Frame(self)
        self.header_frame.pack(side='top')
        self.configure_header_frame()

        self.image_frame = Frame(self)
        self.image_frame.pack()
        self.configure_image_frame()

        self.tools_frame = Frame(self, highlightbackground="gray", highlightthickness=1)
        self.tools_frame.pack(side='bottom', pady=20)
        self.tools_frame.place(x=0, y=global_height/3*2, width=global_width)
        self.configure_tools_frame(self.tools_frame)
    
    '''
    Bulid Header Frame
    '''
    def configure_header_frame(self):
        self.open_image_button = Button(self.header_frame, width=15, height=2, text='Open an image', command=self.open_image)
        self.open_image_button.pack(pady=20)

    def open_image(self):
        # choose an new image path
        self.img_path =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (
            ("pbm file", "*.pbm"), 
            ("all files","*.*"),
            ("jpeg files","*.jpg")))
        # Display the new image in the frame
        self.img = ImageTk.PhotoImage(Image.open(self.img_path))
        self.image_label.configure(image=self.img)
        # Update image information
        width, height = Image.open(self.img_path).size
        self.img_info.configure(text=f"{width} x {height}")
    
    '''
    Bulid Image Frame
    '''
    def configure_image_frame(self):
        # update the initial image
        self.img = ImageTk.PhotoImage(Image.open(self.img_path))
        self.image_label = Label(self.image_frame, image=self.img)
        self.image_label.pack()
        # Image Infor Label
        width, height = Image.open(self.img_path).size
        self.img_info = Label(self.image_frame, text=f"{width} x {height}")
        self.img_info.pack()

    '''
    Bulid Tools Frame
    '''
    def configure_tools_frame(self, tools_frame):
        # Build the resize frame with labels and button
        self.resize_frame = Frame(tools_frame, highlightbackground="green", highlightthickness=1)
        self.add_resize_tool(self.resize_frame)
        self.resize_frame.pack(pady=5)

        # Build the frame for zooming and shrinking
        self.zoom_shrink_frame = Frame(tools_frame, highlightbackground="green", highlightthickness=1)
        self.build_zoom_shrink_frame(self.zoom_shrink_frame)
        self.zoom_shrink_frame.pack(padx=5, pady=5)

        # Build the gray level frame with labels and button
        self.gray_level_frame = Frame(tools_frame, highlightbackground="green", highlightthickness=1)
        self.add_gray_level_controller(self.gray_level_frame)
        self.gray_level_frame.pack(pady=5)
    
    def add_resize_tool(self, resize_frame):
        width_lable = Label(resize_frame, text="width").pack(side=LEFT)
        self.width_input = Text(resize_frame, width=4, height=1, highlightbackground='black', highlightthickness=1)
        self.width_input.pack(side=LEFT)
        height_label = Label(resize_frame, text="height").pack(side=LEFT)
        self.height_input = Text(resize_frame, width=4, height=1, highlightbackground='black', highlightthickness=1)
        self.height_input.pack(side=LEFT)
        self.resize_button = Button(resize_frame, text="Resize", command=self.resize_image)
        self.resize_button.pack(side=LEFT)

    def resize_image(self):
        # Resize the opend image
        width = int(self.width_input.get('1.0', END))
        height = int(self.height_input.get('1.0', END))
        modified_img = Image.open(self.img_path).resize((width, height))
        self.img = ImageTk.PhotoImage(modified_img)
        # Update image information
        self.image_label.configure(image=self.img)
        self.img_info.configure(text=f"{width} x {height}")

    def build_zoom_shrink_frame(self, zoom_shrink_frame):
        zoom_shrink_scale = Scale(zoom_shrink_frame, label='Zoom Shrink Scale', from_=0, to=5, orient=HORIZONTAL,
             length=300, showvalue=1, tickinterval=1, resolution=0.01, command=self.activate_zoom_shrink) 
        zoom_shrink_scale.set(1)
        zoom_shrink_scale.pack()
    
    def activate_zoom_shrink(self, value):
        print(f'zoom and shrink: {value}')

    def add_gray_level_controller(self, gray_level_frame):
        gray_level_label = Label(gray_level_frame, text="Gray Level").pack(side=LEFT)
        self.gray_level_input = Text(gray_level_frame, width=2, height=1, highlightbackground='black', highlightthickness=1)
        self.gray_level_input.pack(side=LEFT)
        self.gray_level_button = Button(gray_level_frame, text="Change gray level", command=self.change_gray_level)
        self.gray_level_button.pack(side=LEFT)
    
    def change_gray_level(self):
        print('gray level')

def main():
    root = Tk()
    app = Window(root)
    root.wm_title("Image Processor")
    root.geometry(f"{global_width}x{global_height}")
    root.mainloop()

if __name__ == '__main__':
    main()
