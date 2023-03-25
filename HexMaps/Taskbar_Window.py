import tkinter as tk
from tkinter import filedialog
from Map_Handler import Map_Handler

class Txt_Btn_Input_Integer:
    def __init__(self, root, title, btn_command, get_img_id, btn_text=""):
        self.frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray")
        self.btn_command = btn_command
        self.get_img_id = get_img_id
        self.title_lbl = tk.Label(self.frame, text=title)
        self.txt = tk.Text(self.frame, height=1, width=10)
        self.btn = tk.Button(self.frame, command = self.btn_pressed, text = btn_text )
        self.tile_img = tk.PhotoImage(file=f"hex_tiles/{get_img_id()}.png")
        self.tile_img = self.tile_img.subsample(int(self.tile_img.width() / 56.7), int(self.tile_img.height() // 65.5))
        self.lbl = tk.Label(self.frame, image=self.tile_img)
        self.open_img_btn = tk.Button(self.frame, text="Select PNG File", command=self.open_file_dialog)
    
    # Define a function to handle button click
    def open_file_dialog(self):
        # Open a file dialog box to select a file
        filename = filedialog.askopenfilename(
            initialdir="./hex_tiles", 
            title="Select File", 
            filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")]
        )
        if filename:
            # If a file was selected, extract the filename and print it
            basename = filename.split("/")[-1]  # Split the path and get the last item
            if basename.endswith(".png"):
                name = basename[:-4]
                self.btn_command(int(name))
                self.update_img()
    

    def update_img(self):
        self.tile_img = tk.PhotoImage(file=f"hex_tiles/{self.get_img_id()}.png")
        self.tile_img = self.tile_img.subsample(int(self.tile_img.width() / 56.7), int(self.tile_img.height() // 65.5))
        self.lbl.configure(image=self.tile_img)

    def btn_pressed(self):
        self.btn_command(int(self.txt.get("1.0", tk.END)))
        self.update_img()

    def grid(self, row, column):
        self.title_lbl.grid(row=0, column=0, columnspan=2)
        self.txt.grid(row=1, column=0, sticky="NEWS")
        self.btn.grid(row=1, column=1, sticky="NEWS")
        self.lbl.grid(row=2, column=0, sticky="NEWS")
        self.open_img_btn.grid(row=2, column=1, sticky="NEWS")
        
        self.frame.grid(row=row, column=column)

class Control_Panel:
    def __init__(self, root, new_map_fct, open_fct, save_fct):
        self.frame = tk.Frame(root, highlightthickness=1, highlightbackground="gray")
        self.BTN_NEW_MAP = tk.Button(self.frame, text = "New Map", command = new_map_fct)
        self.BTN_OPEN_MAP = tk.Button(self.frame, text = "Open Map", command = open_fct)
        self.BTN_SAVE_MAP = tk.Button(self.frame, text = "Save Map", command = save_fct)

    def grid(self, row, column, columnspan=2):
        self.BTN_NEW_MAP.grid(row=0, column=0, sticky="NEWS")
        self.BTN_OPEN_MAP.grid(row=0, column=1, sticky="NEWS")
        self.BTN_SAVE_MAP.grid(row=0, column=2, sticky="NEWS")

        self.frame.grid(row=row, column=column, columnspan=columnspan)

class Taskbar_Window:
    def __init__(self, MAP_HANDLER, TITLE = "Hexmap Tools"): 
        self.MAP_HANDLER = MAP_HANDLER
        self.ROOT = tk.Tk()
        self.ROOT.title(TITLE)

        self.control_panel = Control_Panel(self.ROOT, self.MAP_HANDLER.new_map, self.open_map, self.save_map)
        self.control_panel.grid(row=0, column=0, columnspan=2)

        self.inputs_key_to_tile = [Txt_Btn_Input_Integer(self.ROOT, f"Keybind for key {i}", lambda inp, i=i: self.MAP_HANDLER.change_key_to_tile(i, inp), lambda i=i: self.MAP_HANDLER.get_key_to_tile(i), btn_text = f"Change Keybind") for i in range(10)]
        for k, inp in enumerate(self.inputs_key_to_tile): 
            inp.grid(row = k%5 + 1, column=k//5)


    def save_map(self):
        # Open a file dialog box to select a file
        filename = filedialog.asksaveasfilename(
            initialdir="./maps", 
            initialfile="", 
            title="Select File", 
            filetypes=[("MAP files", "*.data"), ("All Files", "*.*")]
        )
        if filename:
            # If a file was selected, extract the filename and print it
            basename = filename.split("/")[-1]  # Split the path and get the last item
            if basename.endswith(".data"):
                print(basename)
                self.MAP_HANDLER.save_map_to_file(basename)

    def open_map(self):
    # Open a file dialog box to select a file
        filename = filedialog.askopenfilename(
            initialdir="./maps", 
            title="Select File", 
            filetypes=[("MAP files", "*.data"), ("All Files", "*.*")]
        )
        if filename:
            # If a file was selected, extract the filename and print it
            basename = filename.split("/")[-1]  # Split the path and get the last item
            if basename.endswith(".data"):
                self.MAP_HANDLER.load_map_from_file(basename)

    def update(self):
        self.ROOT.update()
    
    def destroy(self):
        self.ROOT.destroy()