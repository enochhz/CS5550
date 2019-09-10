import img_processor
import numpy
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from skimage.io import imread

global_width, global_height = 800, 800

class Window(Frame):

    # top frames
    header_frame, image_frame, tools_frame = "", "", ""

    # tools frame items
    resize_frame = ""
    width_input, height_input  = "", ""
    zooming_algorithms_list = {
        'PIL Library': 'P',
        'The Nearest Neighbor': 'N',
        'Linear Method (x)': 'LX',
        'Linear Method (y)': 'LY',
        'Bilinear Interpolation': 'BL'
    }
    zooming_algorithm, zooming_algorithm_input = "", ""
    resize_button = ""

    gray_level_frame = ""
    gray_level = ""
    gray_level_button = "", ""

    # header frame items
    zoom_shrink_frame = ""
    zoom_shrink_scale = ""
    open_image_button = ""
    image_name_input = ""
    save_image_button = ""

    # image frame items
    image_label, img_path = "", "../static/lena512.pbm"
    ori_img = Image.open(img_path)
    display_img, img_info = "", ""
    img_array = ""
    img_width, img_height = ori_img.size
    modified_img = ""

    # image attribute
    img_array = imread(img_path)
    new_width, new_height = ori_img.size

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.add_main_frames()

    def add_main_frames(self):
        # Build tools frame
        self.tools_frame = Frame(self, highlightbackground="black", highlightthickness=1)
        self.tools_frame.pack(padx=10, pady=10)
        self.tools_frame.place(x=0, y=0, width=global_width, height=100)
        self.configure_tools_frame(self.tools_frame)
        # Build header frame
        self.header_frame = Frame(self)
        self.header_frame.pack(padx=20, pady=20)
        self.header_frame.place(x=0, y=100, width=global_width, height=100)
        self.configure_header_frame()
        # Build image frame
        self.image_frame = Frame(self)
        self.image_frame.pack(padx=10, pady=10)
        self.image_frame.place(x=0, y=200, width=global_width)
        self.initialize_image_frame()
    
    '''
    Bulid Tools Frame
    '''
    def configure_tools_frame(self, tools_frame):
        # Build the resize frame with labels and button
        self.resize_frame = Frame(tools_frame)
        self.add_resize_tool(self.resize_frame)
        self.resize_frame.pack(pady=5)

        # Build the gray level frame with labels and button
        self.gray_level_frame = Frame(tools_frame)
        self.add_gray_level_controller(self.gray_level_frame)
        self.gray_level_frame.pack(pady=5)

    '''
    Build resize tool
    '''
    def add_resize_tool(self, resize_frame):
        width_lable = Label(resize_frame, text="width").pack(side=LEFT)
        self.width_input = Text(resize_frame, width=4, height=1, highlightbackground='black', highlightthickness=1)
        self.width_input.pack(side=LEFT)
        height_label = Label(resize_frame, text="height").pack(side=LEFT)
        self.height_input = Text(resize_frame, width=4, height=1, highlightbackground='black', highlightthickness=1)
        self.height_input.pack(side=LEFT)
        # Set default values of inputs
        self.ori_img = Image.open(self.img_path)
        self.new_width, self.new_height = self.ori_img.size
        self.width_input.insert(END, self.new_width)
        self.height_input.insert(END, self.new_height)
        # Initialize algorithms drop down menu and resize button
        self.zooming_algorithm = StringVar(resize_frame)
        self.zooming_algorithm.set("PIL Library") # default value
        algorithms = list(self.zooming_algorithms_list.keys())
        self.zooming_algorithm_input = OptionMenu(resize_frame, self.zooming_algorithm, algorithms[0], algorithms[1], algorithms[2], algorithms[3], algorithms[4])
        self.zooming_algorithm_input.pack(side=LEFT)
        self.resize_button = Button(resize_frame, text="Resize", command=self.resize_image)
        self.resize_button.pack(side=LEFT)

    def resize_image(self):
        algorithm = self.zooming_algorithms_list[self.zooming_algorithm.get()]
        self.new_width = int(self.width_input.get('1.0', END))
        self.new_height = int(self.height_input.get('1.0', END))
        # Get chosen algorithms and update the image
        new_img = self.get_new_size_img(algorithm, self.new_width, self.new_height)
        self.update_image(new_img) 
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0) 
     
    def get_new_size_img(self, algorithm, width, height):
        if algorithm == 'P':
            return Image.open(self.img_path).resize((width, height))
        elif algorithm == 'N':
            new_img_array = img_processor.nearestNeighbor(self.img_array, width, height)
            return Image.fromarray(new_img_array.astype('uint8'))
        elif algorithm == 'BL':
            new_img_array = img_processor.bilinear(self.img_array, width, height)
            return Image.fromarray(new_img_array.astype('uint8'))

    '''
    Build gray level controller
    '''
    def add_gray_level_controller(self, gray_level_frame):
        gray_level_label = Label(gray_level_frame, text="Bits").pack(side=LEFT)
        self.gray_level = StringVar(gray_level_frame)
        self.gray_level.set("8") # default value
        self.gray_level_input = OptionMenu(gray_level_frame, self.gray_level, "1", "2", "3", "4", "5", "6", "7", "8")
        self.gray_level_input.pack(side=LEFT)
        self.gray_level_button = Button(gray_level_frame, text="Change gray level", command=self.change_gray_level)
        self.gray_level_button.pack(side=LEFT)
    
    def change_gray_level(self):
        self.update_image(self.get_new_size_img('P', self.new_width, self.new_height))
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0)

    '''
    Build zoom and shrink tool
    '''
    def build_zoom_shrink_frame(self, zoom_shrink_frame):
        self.zoom_shrink_scale = Scale(zoom_shrink_frame, label='Zoom Shrink Scale', from_=0, to=5, orient=HORIZONTAL,
             length=300, showvalue=1, tickinterval=1, resolution=0.01, command=self.activate_zoom_shrink) 
        self.zoom_shrink_scale.set(1)
        self.zoom_shrink_scale.pack()
    
    def activate_zoom_shrink(self, value):
        new_width = int(float(self.new_width) * float(value))
        new_height = int(float(self.new_height) * float(value))
        self.modfied_img = self.modified_img.resize((new_width, new_height))
        self.display_img = ImageTk.PhotoImage(self.modfied_img)
        # Update image information
        self.image_label.configure(image=self.display_img)
        self.img_info.configure(text=f"{new_width} x {new_height}")

    '''
    Bulid Header Frame
    '''
    def configure_header_frame(self):
        self.open_image_button = Button(self.header_frame, height=1, text='Open an image', command=self.open_image)
        self.open_image_button.pack(padx=5, side=LEFT)
        # Button for saving the image
        self.image_name_input = Entry(self.header_frame, width=12, textvariable=StringVar(value='new_filename.ext'), highlightbackground='black', highlightthickness=1)
        self.image_name_input.pack(side=LEFT)
        self.save_image_button = Button(self.header_frame, height=1, text='Save the image', command=self.save_image)
        self.save_image_button.pack(padx=5, side=LEFT)
        # Build the frame for zooming and shrinking
        self.zoom_shrink_frame = Frame(self.header_frame)
        self.build_zoom_shrink_frame(self.zoom_shrink_frame)
        self.zoom_shrink_frame.pack(padx=5, pady=5, side=RIGHT)

    def open_image(self):
        # choose an new image path
        self.img_path =  filedialog.askopenfilename(initialdir = "../static",title = "Select file",filetypes = (
            ("pbm file", "*.pbm"), 
            ("all files","*.*"),
            ("jpeg files","*.jpg")))
        self.gray_level.set("8")
        # self.update_image(Image.open(self.img_path))
        self.ori_img = Image.open(self.img_path)
        self.img_array = imread(self.img_path)
        self.new_width, self.new_height = self.ori_img.size
        self.update_image(self.ori_img)
        # Update width and heighter contoller and bits controller
        self.width_input.delete(1.0, END)
        self.width_input.insert(END, self.new_width)
        self.height_input.delete(1.0, END)
        self.height_input.insert(END, self.new_height)
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0)

    def save_image(self):
        new_file_name = self.image_name_input.get()
        self.modified_img.save("../static/new_images/" + new_file_name)
        print(f"Save new file: {new_file_name}")
    
    '''
    Bulid Image Frame
    '''
    def initialize_image_frame(self):
        # Image Info
        self.img_info = Label(self.image_frame)
        self.img_info.pack()
        # Image Displaying Label
        self.image_label = Label(self.image_frame)
        self.image_label.pack()
        self.update_image(Image.open(self.img_path))
    
    def update_image(self, img):
        gray_level = self.gray_level.get()
        self.modified_img = img
        new_array = numpy.array(img)
        new_img_array = img_processor.convertGrayLevel(new_array, 8, int(gray_level))
        self.modified_img = Image.fromarray(new_img_array)
        # Update the resolution label
        self.img_info.configure(text=f"{self.new_width} x {self.new_height}")
        # Updae the image
        self.display_img = ImageTk.PhotoImage(self.modified_img)
        self.image_label.configure(image=self.display_img)

def main():
    root = Tk()
    app = Window(root)
    root.wm_title("Image Processor")
    root.geometry(f"{global_width}x{global_height}")
    root.mainloop()

if __name__ == '__main__':
    main()
