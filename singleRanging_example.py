import vl53l0x


def print_pal_error(status):
    errStr = vl53l0x.ErrorString()
    vl53l0x.VL53L0X_GetPalErrorString(status, errStr)
    print("API Status: {:d} : {}".format(status, errStr))


def rangingText(MyDevice):
    status = vl53l0x.ERROR_NONE

    if status == vl53l0x.ERROR_NONE:
        print("Call of VL53L0X_StaticInit")
        status = VL53L0X_StaticInit(MyDevice)
        print_pal_error(status)
    
    if status == vl53l0x.ERROR_NONE:
        print("Call of VL53L0X_PerformRefCalibration")
        status = VL53L0X_PerformRefCalibration(MyDevice, VhvSettings, PhaseCal)
        print_pal_error(status)
    
    if status == vl53l0x.ERROR_NONE:
        print("Call of VL53L0X_PerformRefSpadManagement")
        status = VL53L0X_PerformRefSpadManagement(MyDevice, refSpadCount, isApertureSpads)
        print("refSpadCount = {:d}, isApertureSpads = {:d}".format(refSpadCount, isApertureSpads))
        print_pal_status(status)
    
    if status == vl53l0x.ERROR_NONE:
        # no need to do this when we use VL53L0X_PerformSingleRangingMeasurement
        print("Call of VL53L0X_SetDeviceMode")
        status = VL53L0X_SetDeviceMode(MyDevice, vl53l0x.DEVICEMODE_SINGLE_RANGING)
        print_pal_error(status)
    
    # Enable/Disable Sigma and Signal check
    if status == vl53l0x.ERROR_NONE:
        status = VL53L0X_SetLimitCheckEnable(MyDevice, vl53l0x.CHECKENABLE_SIGMA_FINAL_RANGE, 1)

    if status == vl53l0x.ERROR_NONE:
        status = VL53L0X_SetLimitCheckEnable(MyDevice, vl53l0x.CHECKENABLE_SIGNAL_RATE_FINAL_RANGE, 1)

    if status == vl53l0x.ERROR_NONE:
        status = VL53L0X_SetLimitCheckEnable(MyDevice, vl53l0x.CHECKENABLE_RANGE_IGNORE_THRESHOLD, 1)
    
    if status == vl53l0x.ERROR_NONE:
        status = VL53L0X_SetLimitCheckValue(MyDevice, vl53l0x.CHECKENABLE_RANGE_IGNORE_THRESHOLD, int(1.5*0.023*65536))
    

    if status == vl53l0x.ERROR_NONE:
        for i in range(10):
            print("Call of VL53L0X_PerformSingleRangingMeasurement")
            status = VL53L0X_PerformSingleRangingMeasurement(MyDevice, RangingMeasurementData)
            print_pal_error(status)
            print_range_status(RangingMeasurementdata)

            VL53L0X_GetLimitCheckCurrent(MyDevice, vl53l0x.CHECKENABLE_RANGE_IGNORE_THRESHOLD, LimitCheckCurrent)

            print("RANGE IGNORE THRESHOLD: {:f}".format(LimitCheckCurrent/65536.0))

            if status != vl53l0x.ERROR_NONE:
                break
            
            print("Measured distance: {:d}".format(RangingMeasurementdata.RangeMilliMeter))
    
    return status


def main():
    myDevice = dict()
    init_done = 0

    print("VL53L0X Simple Ranging example\n")

    myDevice["i2c_dev_addr"] = 0x52
    myDevice["comms_type"] = 1
    myDevice["comms_speed_khz"] = 400

    status = VL53L0X_i2c_init()
    if status != vl53l0x.ERROR_NONE:
        status = vl53l0x.ERROR_CONTROL_INTERFACE
        init_done = 1
    else:
        print("Init Comms")

    if status == vl53l0x.ERROR_NONE:
        status_int = VL53L0X_GetVersion(pVersion)
        if status_int != 0:
            status = vl53l0x.ERROR_CONTROL_INTERFACE
    
    if status == vl53l0x.ERROR_NONE:
        print("Call of VL53L0X_DataInit")
        status = VL53L0X_DataInit(myDevice)
        print_pal_error(status)
    
    if status == vl53l0x.ERROR_NONE:
        status = VL53L0X_GetDeviceInfo(myDevice, DeviceInfo)
        if status == vl53l0x.ERROR_NONE:
            print("VL53L0X_GetDeviceInfo:")
            print("Device Name: {}".format(DeviceInfo.Name))
            print("Device Type: {}".format(DeviceInfo.Type))
            print("Device ID: {}".format(DeviceInfo.ProductId))
            print("ProductRevisionMajor: {}".format(DeviceInfo.ProductRevisionMajor))
            print("ProductRevisionMinor: {}".format(DeviceInfo.ProductRevisionMinor))
        
        if DeviceInfo.ProductRevisionMinor != 1 and DeviceInfo.ProductRevisionMinor != 1:
            print("Error expected cut 1.1 but found cut {:d}.{:d}".format(DeviceInfo.ProductRevisionMajor, DeviceInfo.ProductRevisionMinor))
            status = vl53l0x.ERROR_NOT_SUPPORTED
        print_pal_error(status)
    
    if status == vl53l0x.ERROR_NONE:
        status = rangingText(myDevice)
    
    print_pal_error(status)

    if init_done == 0:
        print("Close Comms")
        status_int = VL53L0X_comms_close()
        if status_int != 0:
            status = vl53l0x.ERROR_CONTROL_INTERFACE
    
    print_pal_error(status)
