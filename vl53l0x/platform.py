from smbus import SMBus
import time
from .defines import *


STATUS_OK = 0
STATUS_FAIL = 1
BYTES_PER_WORD = 2
BYTES_PER_DWORD = 4

i2c_bus_number = 8
# i2c_address = 0x29

i2cbus = SMBus(i2c_bus_number)   # Create a new I2C bus


def PALDevDataGet(Dev:VL53L0X_Device, field):
    return Dev.Data[field]


def PALDevDataSet(Dev:VL53L0X_Device, field, data):
    Dev.Data[field] = data


def VL53L0X_write_multi(address, index:int, data:list, count):
    status = STATUS_OK

    i2c_addr = address >> 1
    if count == 1:
        i2cbus.write_byte_data(i2c_addr, index, data[0])
    else:
        i2cbus.write_i2c_block_data(i2c_addr, index, data)

    return status


def VL53L0X_write_byte(address, index:int, data:list):
    status = STATUS_OK

    status = VL53L0X_write_multi(address, index, data, 1)
    return status


def VL53L0X_read_word(address, index:int, data:IntData):
    status = STATUS_OK

    i2c_addr = address >> 1
    byte_data = i2cbus.read_i2c_block_data(i2c_addr, index, BYTES_PER_WORD)
    data.value = ((byte_data[0] << 8) + byte_data[1])

    return status


def VL53L0X_read_dword(address, index:int, data:IntData):
    status = STATUS_OK

    i2c_addr = address >> 1
    byte_data = i2cbus.read_i2c_block_data(i2c_addr, index, BYTES_PER_DWORD)
    data.value = ((byte_data[0]<<24) + (byte_data[1]<<16) + (byte_data[2]<<8) + byte_data[3])

    return status


def VL53L0X_WrByte(Dev:VL53L0X_Device, index:int, data):
    status = int(VL53L0X_ERROR_NONE)

    i2c_addr = Dev.I2cDevAddr >> 1
    if type(data).__name__ == "int":
        byte_data = data
    elif type(data).__name__ == "IntData":
        byte_data = data.value
    else:
        raise Exception("Invalid data type : {}".format(type(data).__name__))
    i2cbus.write_byte_data(i2c_addr, index, byte_data)
    
    return status


def VL53L0X_RdByte(Dev:VL53L0X_Device, index:int, data:IntData):
    status = int(VL53L0X_ERROR_NONE)

    i2c_addr = Dev.I2cDevAddr >> 1
    i2cbus.write_byte(i2c_addr, index)
    byte_data = i2cbus.read_byte(i2c_addr)
    data.value = byte_data
    
    return status


def VL53L0X_RdWord(Dev:VL53L0X_Device, index:int, data:IntData):
    status = VL53L0X_ERROR_NONE

    status_int = VL53L0X_read_word(Dev.I2cDevAddr, index, data)
    if status_int != 0:
        status = VL53L0X_ERROR_CONTROL_INTERFACE

    return status


def VL53L0X_RdDWord(Dev:VL53L0X_Device, index:int, data:IntData):
    status = VL53L0X_ERROR_NONE

    status_int = VL53L0X_read_dword(Dev.I2cDevAddr, index, data)
    if status_int != 0:
        status = VL53L0X_ERROR_CONTROL_INTERFACE
    
    return status
    

def VL53L0X_PollingDelay(Dev:VL53L0X_Device):
    status = VL53L0X_ERROR_NONE

    begin_time = time.perf_counter()
    elapsed_time = time.perf_counter() - begin_time
    while elapsed_time < 0.001:
        elapsed_time = time.perf_counter() - begin_time
    
    return status