import numpy
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial

import img_processor

global_width, global_height = 780, 800

class Window(Frame):

    # functionality frame attributes
    width_input, height_input  = "", ""
    zooming_algorithms_list = {
        'Nearest Neighbor': 'N',
        'Linear Method (x)': 'LX',
        'Linear Method (y)': 'LY',
        'Bilinear Interpolation': 'BL',
        'PIL Library': 'P'
    }
    zooming_algorithm, zooming_algorithm_input = "", ""
    gray_level = ""

    # image helper attributes
    zoom_shrink_scale = ""
    image_name_input = ""

    # image frame attributes
    image_label, img_path = "", "./static/lena512.pbm"
    ori_img = Image.open(img_path)
    ori_photo_image = ""
    display_img, img_info = "", ""
    img_width, img_height = ori_img.size
    modified_img = ""

    # image attribute
    img_array = numpy.array(Image.open(img_path))
    new_width, new_height = ori_img.size

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.initialize_frames()

    def initialize_frames(self):
        # Initialize meanu
        self.initialize_menu()
        # Initialize functionality frame
        tools_frame = Frame(self, highlightbackground="black", highlightthickness=1)
        tools_frame.pack(padx=10, pady=10)
        tools_frame.place(x=0, y=0, width=global_width, height=80)
        self.initialize_functionality_frame(tools_frame)
        # Initialize image helper frame
        image_helper_frame = Frame(self)
        image_helper_frame.pack(padx=20, pady=20)
        image_helper_frame.place(x=0, y=80, width=global_width, height=100)
        self.initialize_image_helper_frame(image_helper_frame)
        # Initialize image frame
        image_frame = Frame(self)
        image_frame.pack(padx=10, pady=10)
        image_frame.place(x=0, y=180, width=global_width)
        self.initialize_image_frame(image_frame)
    
    '''
    Initialize menu
    '''
    def initialize_menu(self):
        menu = Menu(self)
        self.master.config(menu=menu)
        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Image", command=self.open_image)
        fileMenu.add_command(label="Save Image", command=self.save_image) 
    
    '''
    Bulid Tools Frame
    '''
    def initialize_functionality_frame(self, tools_frame):
        # Build the resize frame with labels and button
        resize_frame = Frame(tools_frame)
        self.add_resize_tool(resize_frame)
        resize_frame.pack(pady=5)

        # Build the gray level frame with labels and button
        gray_level_frame = Frame(tools_frame)
        self.add_gray_level_controller(gray_level_frame)
        gray_level_frame.pack(pady=5)

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
        self.zooming_algorithm.set("Nearest Neighbor") # default value
        algorithms = list(self.zooming_algorithms_list.keys())
        self.zooming_algorithm_input = OptionMenu(resize_frame, self.zooming_algorithm, algorithms[0], algorithms[1], algorithms[2], algorithms[3], algorithms[4])
        self.zooming_algorithm_input.pack(side=LEFT)
        resize_button = Button(resize_frame, text="Resize", command=self.resize_image)
        resize_button.pack(side=LEFT)

    '''
    Build gray level controller
    '''
    def add_gray_level_controller(self, gray_level_frame):
        gray_level_label = Label(gray_level_frame, text="Bits").pack(side=LEFT)
        self.gray_level = StringVar(gray_level_frame)
        self.gray_level.set("8") # default value
        self.gray_level_input = OptionMenu(gray_level_frame, self.gray_level, "1", "2", "3", "4", "5", "6", "7", "8")
        self.gray_level_input.pack(side=LEFT)
        gray_level_button = Button(gray_level_frame, text="Change gray level", command=self.change_gray_level)
        gray_level_button.pack(side=LEFT)

    '''
    Bulid Image Helper Frame
    '''
    def initialize_image_helper_frame(self, image_helper_frame):
        # Pop up original image
        popup_button = Button(image_helper_frame, text="Original Image", command=self.popup_original_image)
        popup_button.pack(side=LEFT)

        # Button for histogram displaying
        display_histogram_button = Button(image_helper_frame, text='Histogram Diagram')
        display_histogram_button.pack(padx=5, side=LEFT)

        # Build the frame for zooming and shrinking
        zoom_shrink_frame = Frame(image_helper_frame)
        self.build_zoom_shrink_frame(zoom_shrink_frame)
        zoom_shrink_frame.pack(padx=5, pady=5, side=RIGHT)

    '''
    Build zoom and shrink tool
    '''
    def build_zoom_shrink_frame(self, zoom_shrink_frame):
        self.zoom_shrink_scale = Scale(zoom_shrink_frame, label='Zoom Shrink Scale', from_=0, to=5, orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=1, resolution=0.01, command=self.activate_zoom_shrink) 
        self.zoom_shrink_scale.set(1)
        self.zoom_shrink_scale.pack()

    '''
    Bulid Image Frame
    '''
    def initialize_image_frame(self, image_frame):
        # Image Info
        self.img_info = Label(image_frame)
        self.img_info.pack()
        # Image Displaying Label
        self.image_label = Label(image_frame)
        self.image_label.pack()
        self.update_image(Image.open(self.img_path))
        self.ori_photo_image = ImageTk.PhotoImage(self.ori_img)

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
        elif algorithm == 'LX':
            new_img_array = img_processor.linearX(self.img_array, width, height)
            return Image.fromarray(new_img_array.astype('uint8'))
        elif algorithm == 'LY':
            new_img_array = img_processor.linearY(self.img_array, width, height)
            return Image.fromarray(new_img_array.astype('uint8'))
    
    def change_gray_level(self):
        self.update_image(self.get_new_size_img('P', self.new_width, self.new_height))
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0)

    def activate_zoom_shrink(self, value):
        new_width = int(float(self.new_width) * float(value))
        new_height = int(float(self.new_height) * float(value))
        self.modfied_img = self.modified_img.resize((new_width, new_height))
        self.display_img = ImageTk.PhotoImage(self.modfied_img)
        # Update image information
        self.image_label.configure(image=self.display_img)
        self.img_info.configure(text=f"{new_width} x {new_height}")

    def open_image(self):
        # choose an new image path
        self.img_path =  filedialog.askopenfilename(initialdir = "./static",title = "Select file",filetypes = (
            ("pbm file", "*.pbm"), 
            ("all files","*.*"),
            ("jpeg files","*.jpg")))
        self.gray_level.set("8")
        # update the new image display
        self.ori_img = Image.open(self.img_path)
        self.img_width, self.img_height = self.ori_img.size
        # self.img_array = imread(self.img_path)
        self.img_array = numpy.array(Image.open(self.img_path))
        self.new_width, self.new_height = self.ori_img.size
        self.update_image(self.ori_img)
        # Update width and heighter contoller and bits controller
        self.width_input.delete(1.0, END)
        self.width_input.insert(END, self.new_width)
        self.height_input.delete(1.0, END)
        self.height_input.insert(END, self.new_height)
        self.zoom_shrink_scale['variable'] = DoubleVar(value=1.0)
        self.ori_photo_image = ImageTk.PhotoImage(self.ori_img)
    
    def popup_original_image(self): 
        popup_image_window = Toplevel()
        popup_image_window.wm_title(f"{self.img_path.split('/')[-1]} ({self.img_width} x {self.img_height})")
        popup_image_label = Label(popup_image_window)
        popup_image_label.pack()
        popup_image_label.configure(image=self.ori_photo_image)
        popup_image_label.image = self.ori_photo_image

    def save_image(self):
        popup_save_window = Toplevel()
        popup_save_window.geometry('400x50')
        popup_save_window.wm_title("Save Image")
        file_name_label = Label(popup_save_window, text="New File Name: ")
        file_name_label.pack(padx=10, side=LEFT)
        new_file_name_entry = Entry(popup_save_window, width=12, textvariable=StringVar(value='new_file.pbm'), highlightbackground='black', highlightthickness=1)
        new_file_name_entry.pack(padx=10, side=LEFT)
        save_image_button = Button(popup_save_window, height=1, text='Save Image', command=partial(self.popup_save_image, popup_save_window, new_file_name_entry))
        save_image_button.pack(padx=10, side=RIGHT)
    
    def popup_save_image(self, popup_save_window, new_file_name_entry):
        new_file_name = new_file_name_entry.get()
        popup_save_window.destroy()
        self.modified_img.save("./static/new_images/" + new_file_name)
        messagebox.showinfo(title="Image Saved", message=f"You saved new image in \nstatic/new_images/{new_file_name}")
    
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
