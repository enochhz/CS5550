import os
import numpy
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial

import img_processor

class Window(Frame):
    functionality_frame_width, functionality_frame_height = 450, 50
    image_frame_width, image_frame_height = 780, 700

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
        self.master.geometry(f"{self.functionality_frame_width + self.image_frame_width}x{self.image_frame_height}")
    
    def initialize_frames(self):
        self.initialize_menu()
        self.initialize_image_resize_frame(Frame(self))
        self.initialize_gray_level_frame(Frame(self))
        self.initialize_histogram_equalization_frame(Frame(self))
        self.initialize_spatial_filtering_frame(Frame(self))
        self.initialize_bit_panel_removal_frame(Frame(self))
        self.initialize_image_helper_frame(Frame(self))
        self.initialize_zoom_shrink_frame(Frame(self))
        self.initialize_image_frame(Frame(self))
    
    def initialize_menu(self):
        menu = Menu(self)
        self.master.config(menu=menu)
        fileMenu = Menu(menu)
        menu.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New Image", command=self.open_image)
        fileMenu.add_command(label="Save Image", command=self.save_image) 
    
    def initialize_image_resize_frame(self, image_resize_frame):
        image_resize_frame.place(x=0, y=0, width=self.functionality_frame_width, height=self.functionality_frame_height)
        width_label = Label(image_resize_frame, text="width").pack(side=LEFT)
        self.width_input = Text(image_resize_frame, width=4, height=1, highlightbackground='black', highlightthickness=1)
        self.width_input.pack(side=LEFT)
        height_label = Label(image_resize_frame, text="height").pack(side=LEFT)
        self.height_input = Text(image_resize_frame, width=4, height=1, highlightbackground='black', highlightthickness=1)
        self.height_input.pack(side=LEFT)
        # Set default values of inputs
        self.ori_img = Image.open(self.img_path)
        self.new_width, self.new_height = self.ori_img.size
        self.width_input.insert(END, self.new_width)
        self.height_input.insert(END, self.new_height)
        # Initialize algorithms drop down menu and resize button
        self.zooming_algorithm = StringVar(image_resize_frame)
        self.zooming_algorithm.set("Nearest Neighbor") # default value
        algorithms = list(self.zooming_algorithms_list.keys())
        self.zooming_algorithm_input = OptionMenu(image_resize_frame, self.zooming_algorithm, algorithms[0], algorithms[1], algorithms[2], algorithms[3], algorithms[4])
        self.zooming_algorithm_input.pack(side=LEFT)
        resize_button = Button(image_resize_frame, text="Resize", command=self.resize_image)
        resize_button.pack(side=LEFT)
    
    def initialize_gray_level_frame(self, gray_level_frame):
        gray_level_frame.place(x=0, y=self.functionality_frame_height, width=self.functionality_frame_width, height=self.functionality_frame_height)
        gray_level_label = Label(gray_level_frame, text="Bits").pack(side=LEFT)
        self.gray_level = StringVar(gray_level_frame)
        self.gray_level.set("8") # default value
        self.gray_level_input = OptionMenu(gray_level_frame, self.gray_level, "1", "2", "3", "4", "5", "6", "7", "8")
        self.gray_level_input.pack(side=LEFT)
        gray_level_button = Button(gray_level_frame, text="Change gray level", command=self.change_gray_level)
        gray_level_button.pack(side=LEFT)

    def initialize_histogram_equalization_frame(self, histogram_equalization_frame):
        histogram_equalization_frame.place(x=0, y=self.functionality_frame_height * 2, width=self.functionality_frame_width, height=self.functionality_frame_height)
        # Initialize histogram equalization drop down menu and resize button
        self.histogram_equalization_choice = StringVar(histogram_equalization_frame)
        self.histogram_equalization_choice.set("Global") # default value
        histogram_equalization_options = ['Global', 'Local']
        self.histogram_equalization_menu = OptionMenu(histogram_equalization_frame, self.histogram_equalization_choice, histogram_equalization_options[0], histogram_equalization_options[1])
        self.histogram_equalization_menu.pack(side=LEFT)

        mask_size_input = Text(histogram_equalization_frame, width=3, height=1, highlightbackground='black', highlightthickness=1)
        mask_size_input.pack(side=LEFT)
        # Set default values of inputs
        mask_size_input.insert(END, 3)
        resize_button = Button(histogram_equalization_frame, text="Histogram Equalization", command=self.histogram_equalization)
        resize_button.pack(side=LEFT)
    
    def histogram_equalization(self):
        if self.histogram_equalization_choice.get() == 'Global':
            self.update_image(self.get_new_size_img('P', self.new_width, self.new_height))
            new_img_array = img_processor.global_histogram_equalization(self.img_array)
            self.update_image(Image.fromarray(new_img_array.astype('uint8')))
        else:
            print("Local")

    def initialize_spatial_filtering_frame(self, spatial_filtering_frame):
        spatial_filtering_frame.place(x=0, y=self.functionality_frame_height * 3, width=self.functionality_frame_width, height=self.functionality_frame_height)
        # Initialize algorithms drop down menu and resize button
        self.spatial_filter_choice = StringVar(spatial_filtering_frame)
        self.spatial_filter_choice.set("Smoothing") # default value
        filters = ['Smoothing', 'Median', 'Sharpening', 'Laplcian', 'High-boosting']
        self.filter_option_menu = OptionMenu(spatial_filtering_frame, self.spatial_filter_choice, filters[0], filters[1], filters[2], filters[3])
        self.filter_option_menu.pack(side=LEFT)

        mask_size_input = Text(spatial_filtering_frame, width=3, height=1, highlightbackground='black', highlightthickness=1)
        mask_size_input.pack(side=LEFT)
        # Set default values of inputs
        mask_size_input.insert(END, 3)
        resize_button = Button(spatial_filtering_frame, text="Filtering")
        resize_button.pack(side=LEFT)

    def initialize_bit_panel_removal_frame(self, bit_panel_removal_frame):
        bit_panel_removal_frame.place(x=0, y=self.functionality_frame_height * 4, width=self.functionality_frame_width, height=self.functionality_frame_height)
        bits_label = [1, 2, 3, 4, 5, 6, 7, 8]
        bits_vars = []
        for bit in bits_label:
            var = IntVar()
            check_button = Checkbutton(bit_panel_removal_frame, text=bit, variable=var)
            check_button.pack(side=LEFT)
            bits_vars.append(var)
        resize_button = Button(bit_panel_removal_frame, text="Bit Panel Removal")
        resize_button.pack(side=LEFT)

    def initialize_image_helper_frame(self, image_helper_frame):
        image_helper_frame.pack(padx=20, pady=20)
        image_helper_frame.place(x=0, y=self.functionality_frame_height * 5, width=self.functionality_frame_width, height=self.functionality_frame_height)
        # Pop up original image
        popup_button = Button(image_helper_frame, text="Original Image", command=self.popup_original_image)
        popup_button.pack(side=LEFT)
        # Button for histogram displaying
        display_histogram_button = Button(image_helper_frame, text='Histogram Diagram')
        display_histogram_button.pack(padx=5, side=LEFT)

    def initialize_zoom_shrink_frame(self, zoom_shrink_frame):
        zoom_shrink_frame.place(x=0, y=self.functionality_frame_height * 6, width=self.functionality_frame_width, height=100)
        self.zoom_shrink_scale = Scale(zoom_shrink_frame, label='Zoom Shrink Scale', from_=0, to=5, orient=HORIZONTAL,
             length=400, showvalue=1, tickinterval=1, resolution=0.01, command=self.activate_zoom_shrink) 
        self.zoom_shrink_scale.set(1)
        self.zoom_shrink_scale.pack(side=LEFT)

    def initialize_image_frame(self, image_frame):
        image_frame.pack(padx=10, pady=10)
        image_frame.place(x=self.functionality_frame_width, y=0, width=self.image_frame_width, height=self.image_frame_height)
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
        if not os.path.exists("./static/new_images"):
            os.mkdir('./static/new_images')
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
    root.mainloop()

if __name__ == '__main__':
    main()
