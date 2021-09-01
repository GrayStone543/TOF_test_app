from smbus import SMBus

STATUS_OK = 0
STATUS_FAIL = 1

VL53L0X_REG_RESULT_RANGE_STATUS = 0x0014
VL53L0X_REG_IDENTIFICATION_REVISION_ID = 0x00c2

i2c_bus_number = 8
i2c_address = 0x29

i2cbus = SMBus(i2c_bus_number)   # Create a new I2C bus


def VL53L0X_RdByte(index:int, data:list):
    # status = STATUS_OK
    i2cbus.write_byte(i2c_address, index)
    byte_data = i2cbus.read_byte(i2c_address)
    data.append(byte_data)
    # return status


def VL53L0X_GetProductRevision():
    data_list = []
    VL53L0X_RdByte(VL53L0X_REG_IDENTIFICATION_REVISION_ID, data_list)

    print("len of data_list = {}".format(len(data_list)))
    if len(data_list) > 0:
        print("{}  {}".format(type(data_list[0]), data_list[0]))


def VL53L0X_GetDeviceErrorStatus():
    data_list = []
    VL53L0X_RdByte(VL53L0X_REG_RESULT_RANGE_STATUS, data_list)

    print("len of data_list = {}".format(len(data_list)))
    if len(data_list) > 0:
        print("{}  {}".format(type(data_list[0]), data_list[0]))



if __name__ == "__main__":
    VL53L0X_GetProductRevision()
    # VL53L0X_GetDeviceErrorStatus()