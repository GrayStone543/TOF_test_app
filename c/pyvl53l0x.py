import os
import ctypes


# so_file = os.path.abspath("pyvl53l0x.so")
cur_path = os.path.split(os.path.abspath(__file__))[0]
so_file = os.path.join(cur_path, "pyvl53l0x.so")
c_lib = ctypes.CDLL(so_file)


vl53l0x_open = c_lib.VL53L0X_open
vl53l0x_close = c_lib.VL53L0X_close
perform_ranging_measurement = c_lib.VL53L0X_perform_ranging_measurement
get_range_millimeter = c_lib.VL53L0X_get_range_millimeter
get_range_status = c_lib.VL53L0X_get_range_status
get_range_status_str = c_lib.VL53L0X_get_range_status_str





