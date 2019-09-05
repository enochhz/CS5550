from tkinter import *
from tkinter import filedialog
# pip install pillow
from PIL import ImageTk, Image

global_width, global_height = 1000, 1000 

class Window(Frame):

    toolbar = ""
    open_image_button = ""
    edit_image_button = ""

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        # add function bar
        self.update_tool_bar()

    def update_tool_bar(self):
        self.toolbar = Frame(self)
        button_text = "open an image"
        self.open_image_button = Button(self.toolbar, text = button_text, command = self.file_dialog)
        self.open_image_button.pack(side=LEFT, padx=2, pady=2)
        # edit image button is initially disabled 
        self.edit_image_button = Button(self.toolbar, text = "Edit the image")
        self.edit_image_button.pack(side=LEFT, padx=2, pady=2)
        self.edit_image_button.configure(state=DISABLED)
        self.toolbar.pack(side=TOP, fill=X)

    def file_dialog(self):
        # choose an image and display it
        filename =  filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("pbm file", "*.pbm"), ("all files","*.*"),("jpeg files","*.jpg")))
        self.display_image(filename)

    def display_image(self, path):
        load = Image.open(path)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img_width, img_height = load.size
        img.place(x = (global_width - img_width)/2, y = (global_height - img_height)/2)
        self.edit_image_button.configure(state=NORMAL)

def main():
    root = Tk()
    app = Window(root)
    root.wm_title("Image Editor")
    root.geometry(f"{global_width}x{global_height}")
    root.mainloop()

if __name__ == '__main__':
    main()