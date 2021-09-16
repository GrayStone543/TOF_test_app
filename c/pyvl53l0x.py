import os
import ctypes


class VL53L0X:
    def __init__(self):
        so_fname = os.path.abspath("pyvl53l0x.so")
        self.c_lib = ctypes.CDLL(so_fname)

        VL53L0X_open = self.c_lib.VL53L0X_open
        VL53L0X_open()

    def perform_ranging_measurement(self):
        VL53L0X_perform_ranging_measurement = self.c_lib.VL53L0X_perform_ranging_measurement
        VL53L0X_get_range_millimeter = self.c_lib.VL53L0X_get_range_millimeter
        VL53L0X_get_range_status = self.c_lib.VL53L0X_get_range_status

        status = VL53L0X_perform_ranging_measurement()
        if status == 0:
            self.range_mm = VL53L0X_get_range_millimeter()
            self.range_status = VL53L0X_get_range_status()


    def __del__(self):
        VL53L0X_close = self.c_lib.VL53L0X_close
        VL53L0X_close()

