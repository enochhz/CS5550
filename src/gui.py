import img_processor
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from skimage.io import imread

global_width, global_height = 800, 1000

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

    zoom_shrink_frame = ""
    zoom_shrink_scale = ""

    gray_level_frame = ""
    gray_level = ""
    gray_level_button = "", ""

    # header frame items
    open_image_button = ""
    image_name_input = ""
    save_image_button = ""

    # image frame items
    image_label, img_path, img, img_info = "", "../static/empty_image.png", "", ""
    img_array = ""
    img_width, img_height = "", ""
    modified_img = ""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.add_main_frames()

    def add_main_frames(self):
        # Build tools frame
        self.tools_frame = Frame(self, highlightbackground="gray", highlightthickness=1)
        self.tools_frame.pack(padx=10, pady=10)
        self.tools_frame.place(x=0, y=0, height=200)
        self.configure_tools_frame(self.tools_frame)
        # Build header frame
        self.header_frame = Frame(self)
        self.header_frame.pack(padx=10, pady=10)
        self.header_frame.place(x=0, y=200, height=50)
        self.configure_header_frame()
        # Build image frame
        self.image_frame = Frame(self)
        self.image_frame.pack(padx=10, pady=10)
        self.image_frame.place(x=0, y=250)
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

        # Build the frame for zooming and shrinking
        self.zoom_shrink_frame = Frame(tools_frame)
        self.build_zoom_shrink_frame(self.zoom_shrink_frame)
        self.zoom_shrink_frame.pack(padx=5, pady=5)

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
        self.zooming_algorithm = StringVar(resize_frame)
        self.zooming_algorithm.set("PIL Library") # default value
        algorithms = list(self.zooming_algorithms_list.keys())
        self.zooming_algorithm_input = OptionMenu(resize_frame, self.zooming_algorithm, algorithms[0], algorithms[1], algorithms[2], algorithms[3], algorithms[4])
        self.zooming_algorithm_input.pack(side=LEFT)
        self.resize_button = Button(resize_frame, text="Resize", command=self.resize_image)
        self.resize_button.pack(side=LEFT)

    def resize_image(self):
        algorithm = self.zooming_algorithms_list[self.zooming_algorithm.get()]
        width = int(self.width_input.get('1.0', END))
        height = int(self.height_input.get('1.0', END))
        # Get chosen algorithm and resize the opend image
        if algorithm == 'P':
            self.update_image(Image.open(self.img_path).resize((width, height)))
        elif algorithm == 'N':
            new_img_array = img_processor.nearestNeighbor(self.img_array, width, height)
            self.update_image(Image.fromarray(new_img_array.astype('uint8')))
        elif algorithm == 'BL':
            new_img_array = img_processor.bilinear(self.img_array, width, height)
            self.update_image(Image.fromarray(new_img_array.astype('uint8')))
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0)

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
        new_gray_level = self.gray_level.get()
        new_img_array = img_processor.convertGrayLevel(self.img_array, 8, int(new_gray_level))
        self.modified_img = Image.fromarray(new_img_array)
        self.update_image(self.modified_img)

    '''
    Build zoom and shrink tool
    '''
    def build_zoom_shrink_frame(self, zoom_shrink_frame):
        self.zoom_shrink_scale = Scale(zoom_shrink_frame, label='Zoom Shrink Scale', from_=0, to=5, orient=HORIZONTAL,
             length=300, showvalue=1, tickinterval=1, resolution=0.01, command=self.activate_zoom_shrink) 
        self.zoom_shrink_scale.set(1)
        self.zoom_shrink_scale.pack()
    
    def activate_zoom_shrink(self, value):
        new_width = int(float(self.img_width) * float(value))
        new_height = int(float(self.img_height) * float(value))
        self.modfied_img = self.modified_img.resize((new_width, new_height))
        # self.modfied_img = Image.open(self.img_path).resize((new_width, new_height))
        self.img = ImageTk.PhotoImage(self.modfied_img)
        # Update image information
        self.image_label.configure(image=self.img)
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

    def open_image(self):
        # choose an new image path
        self.img_path =  filedialog.askopenfilename(initialdir = "../static",title = "Select file",filetypes = (
            ("pbm file", "*.pbm"), 
            ("all files","*.*"),
            ("jpeg files","*.jpg")))
        self.update_image(Image.open(self.img_path))
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0)

    def save_image(self):
        new_file_name = self.image_name_input.get()
        self.modified_img.save("../static/new_images/" + new_file_name)
        print(f"Save new file: {new_file_name}")
    
    '''
    Bulid Image Frame
    '''
    def initialize_image_frame(self):
        self.img_info = Label(self.image_frame)
        self.img_info.pack()
        self.image_label = Label(self.image_frame)
        self.image_label.pack()
        self.update_image(Image.open(self.img_path))
    
    def update_image(self, img):
        self.modified_img = img
        self.img_array = imread(self.img_path)
        self.img_width, self.img_height = img.size
        # Update the resolution label
        self.img_info.configure(text=f"{self.img_width} x {self.img_height}")
        # Updae the image
        self.img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self.img)

def main():
    root = Tk()
    app = Window(root)
    root.wm_title("Image Processor")
    root.geometry(f"{global_width}x{global_height}")
    root.mainloop()

if __name__ == '__main__':
    main()
