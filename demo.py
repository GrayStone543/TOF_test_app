import os
import ctypes
import tkinter as tk


cur_path = os.path.split(os.path.abspath(__file__))[0]
so_file = os.path.join(cur_path, "c", "pyvl53l0x.so")
c_lib = ctypes.CDLL(so_file)


vl53l0x_open = c_lib.VL53L0X_open
vl53l0x_close = c_lib.VL53L0X_close
perform_ranging_measurement = c_lib.VL53L0X_perform_ranging_measurement
get_range_millimeter = c_lib.VL53L0X_get_range_millimeter
get_range_status = c_lib.VL53L0X_get_range_status
get_range_status_str = c_lib.VL53L0X_get_range_status_str
get_range_status_str.restype = ctypes.c_char_p


class MainWindow:
    def __init__(self, width=420, height=240):
        self.root = tk.Tk()
        self.root.title("TOF Demo")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry("%dx%d"%(width, height))
        self.root.minsize(width=420, height=240)

        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.bind("<Key>", self.on_key_pressed)

        self.start_btn = tk.Button(self.root, text="Start", command=self.on_start_btn)
        self.start_btn.place(x=20, y=4, width=120, height=28)
        self.stop_btn = tk.Button(self.root, text="Stop", command=self.on_stop_btn)
        self.stop_btn.place(x=150, y=4, width=120, height=28)
        self.range_label = tk.Label(self.root, text="---", anchor=tk.CENTER, borderwidth=3, relief=tk.RIDGE)
        self.range_label.place(x=20, y=36, width=250, height=28)

        self.init_done = False
    
    def on_closing(self):
        if self.init_done:
            self.on_stop_btn()
        self.root.destroy()

    def on_resize(self, event):
        if type(event.widget).__name__ == "Tk":
            new_w, new_h = event.width, event.height
            #print("new window size: {:d} x {:d}".format(new_w, new_h))

    def on_key_release(self, event):
        if event.keysym == "Control_L":
            # L-Ctrl Key
            pass

        if event.char == "i":
            # i Key
            pass
            
    def on_key_pressed(key, event):
        if event.keysym == "Control_L":
            # L-Ctrl Key
            pass

    def on_start_btn(self):
        if not self.init_done:
            vl53l0x_open()
            self.init_done = True
            self.root.after(2000, self.update_range)

    def on_stop_btn(self):
        if self.init_done:
            self.init_done = False
            vl53l0x_close()

    def mainloop(self):
        self.root.mainloop()

    def update_range(self):
        if self.init_done:
            status = perform_ranging_measurement()
            if status == 0:
                range_status = get_range_status()
                if range_status == 0:
                    range_mm = get_range_millimeter()
                    self.range_label.configure(text="{:d} mm".format(range_mm))
                else:
                    bytes_data = get_range_status_str()
                    err_str = bytes_data.decode("ascii")
                    print("range status = {:d}".format(range_status))
                    self.range_label.configure(text=err_str)
            else:
                print("perform ranging status = {:d}".format(status))
            self.root.after(2000, self.update_range)



if __name__ == "__main__":
    mainWnd = MainWindow()
    mainWnd.mainloop()
