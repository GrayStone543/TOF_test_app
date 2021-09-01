from smbus import SMBus
from enum import IntEnum


STATUS_OK = 0
STATUS_FAIL = 1

VL53L0X_REG_RESULT_RANGE_STATUS = 0x0014
VL53L0X_REG_IDENTIFICATION_REVISION_ID = 0x00c2


class ErrorStatus(IntEnum):
    VL53L0X_DEVICEERROR_NONE = 0
    VL53L0X_DEVICEERROR_VCSELCONTINUITYTESTFAILURE = 1
    VL53L0X_DEVICEERROR_VCSELWATCHDOGTESTFAILURE = 2
    VL53L0X_DEVICEERROR_NOVHVVALUEFOUND = 3
    VL53L0X_DEVICEERROR_MSRCNOTARGET = 4
    VL53L0X_DEVICEERROR_SNRCHECK = 5
    VL53L0X_DEVICEERROR_RANGEPHASECHECK = 6
    VL53L0X_DEVICEERROR_SIGMATHRESHOLDCHECK = 7
    VL53L0X_DEVICEERROR_TCC = 8
    VL53L0X_DEVICEERROR_PHASECONSISTENCY = 9
    VL53L0X_DEVICEERROR_MINCLIP = 10
    VL53L0X_DEVICEERROR_RANGECOMPLETE = 11
    VL53L0X_DEVICEERROR_ALGOUNDERFLOW = 12
    VL53L0X_DEVICEERROR_ALGOOVERFLOW = 13
    VL53L0X_DEVICEERROR_RANGEIGNORETHRESHOLD = 14



i2c_bus_number = 8
i2c_address = 0x29

i2cbus = SMBus(i2c_bus_number)   # Create a new I2C bus


def VL53L0X_RdByte(index:int, data:list):
    # status = STATUS_OK
    i2cbus.write_byte(i2c_address, index)
    byte_data = i2cbus.read_byte(i2c_address)
    data.append(byte_data)
    # return status


def VL53L0X_GetProductRevision(version:dict):
    status = STATUS_OK

    data_list = []
    VL53L0X_RdByte(VL53L0X_REG_IDENTIFICATION_REVISION_ID, data_list)

    # print("len of data_list = {}".format(len(data_list)))

    if len(data_list) > 0:
    #     print("{}  {}".format(type(data_list[0]), data_list[0]))
        version["major"] = 1
        version["minor"] = (data_list[0] & 0xf0) >> 4
    else:
        status = STATUS_FAIL

    return status


def VL53L0X_GetDeviceErrorStatus(dev_data:dict):
    status = STATUS_OK

    data_list = []
    VL53L0X_RdByte(VL53L0X_REG_RESULT_RANGE_STATUS, data_list)

    # print("len of data_list = {}".format(len(data_list)))

    if len(data_list) > 0:
        # print("{}  {}".format(type(data_list[0]), data_list[0]))
        dev_data["err status"] = (data_list[0] & 0x78) >> 3
    else:
        status = STATUS_FAIL
    
    return status


def VL53L0X_GetPowerMode(dev_data:dict):
    status = STATUS_OK

    data_list = []
    VL53L0X_RdByte(0x80, data_list)

    # print("len of data_list = {}".format(len(data_list)))

    if len(data_list) > 0:
        # print("{}  {}".format(type(data_list[0]), data_list[0]))
        if data_list[0] == 1:
            dev_data["power mode"] = "IDLE"
        else:
            dev_data["power mode"] = "STANDBY"
    else:
        status = STATUS_FAIL
    return status


if __name__ == "__main__":
    dev_data = dict()
    ret = VL53L0X_GetProductRevision(dev_data)
    if ret == STATUS_OK:
        print("Version: {}.{}".format(dev_data["major"], dev_data["minor"]))

    ret = VL53L0X_GetPowerMode(dev_data)
    if ret == STATUS_OK:
        print("Power Mode={}".format(dev_data["power mode"]))

    ret = VL53L0X_GetDeviceErrorStatus(dev_data)
    if ret == STATUS_OK:
        print("dev err status = {}".format(dev_data["err status"]))
    
