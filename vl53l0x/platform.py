from smbus import SMBus
from defines import *


STATUS_OK = 0
STATUS_FAIL = 1

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


def VL53L0X_read_word(address, index:int, data:list):
    status = STATUS_OK

    i2c_addr = address >> 1
    byte_data = i2cbus.read_i2c_block_data(i2c_addr, index, 2)
    data.append((byte_data[0] << 8) + byte_data[1])

    return status


def VL53L0X_WrByte(Dev:VL53L0X_Device, index:int, data:list):
    status = ERROR_NONE

    i2c_addr = Dev.I2cDevAddr >> 1
    i2cbus.write_byte_data(i2c_addr, index, data[0])
    
    return status


def VL53L0X_RdByte(Dev:VL53L0X_Device, index:int, data:list):
    status = ERROR_NONE

    i2c_addr = Dev.I2cDevAddr >> 1
    i2cbus.write_byte(i2c_addr, index)
    byte_data = i2cbus.read_byte(i2c_addr)
    data.append(byte_data)
    
    return status


def VL53L0X_RdWord(Dev:VL53L0X_Device, index:int, data:list):
    status = ERROR_NONE

    status_int = VL53L0X_read_word(Dev.I2cDevAddr, index, data)
    if status_int != 0:
        status = ERROR_CONTROL_INTERFACE

    return status