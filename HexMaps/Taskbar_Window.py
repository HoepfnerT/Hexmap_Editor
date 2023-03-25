import tkinter as tk



class Txt_Btn_Input_Integer:
    def __init__(self, root, command, btn_text=""):
        self.frame = tk.Frame(root)
        self.txt = tk.Text(self.frame, height=1, width=10)
        self.btn = tk.Button(self.frame, command = lambda: command(int(self.txt.get("1.0", tk.END))), text = btn_text )
    def grid(self, row, column):
        self.txt.grid(row=0, column=0)
        self.btn.grid(row=0, column=1)
        self.frame.grid(row=row, column=column)


class Taskbar_Window:
    def __init__(self, GAME_WINDOW, TITLE = "Pilz' HexViewer Tools"): 
        self.GAME_WINDOW = GAME_WINDOW
        self.ROOT = tk.Tk()
        self.ROOT.title(TITLE)

        self.BTN_NEW_MAP = tk.Button(self.ROOT, text = "New Map", command = self.GAME_WINDOW.new_map)
        self.BTN_NEW_MAP.grid()


        self.inputs_key_to_tile = [Txt_Btn_Input_Integer(self.ROOT, lambda inp, i=i: self.GAME_WINDOW.change_key_to_tile(i, inp), btn_text = f"Change Keybind {i}.") for i in range(10)]
        for k, inp in enumerate(self.inputs_key_to_tile): 
            inp.grid(row = k, column=0)

    def update(self):
        self.ROOT.update()
    