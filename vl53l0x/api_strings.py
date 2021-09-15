from .defines import *


STRING_UNKNOW_ERROR_CODE            = "Unknow Error Code"

ErrorStringDict = {
    VL53L0X_ERROR_NONE:                 "No Error",
    VL53L0X_ERROR_CALIBRATION_WARNING:  "Calibration Warning Error",
    VL53L0X_ERROR_MIN_CLIPPED:          "Min clipped error",
    VL53L0X_ERROR_UNDEFINED:            "Undefined error",
    VL53L0X_ERROR_INVALID_PARAMS:       "Invalid parameters error",
    VL53L0X_ERROR_NOT_SUPPORTED:        "Not supported error",
    VL53L0X_ERROR_RANGE_ERROR:          "Range error",
    VL53L0X_ERROR_TIME_OUT:             "Time out error",
    VL53L0X_ERROR_MODE_NOT_SUPPORTED:   "Mode not supported error",
    VL53L0X_ERROR_BUFFER_TOO_SMALL:     "Buffer too small",
    VL53L0X_ERROR_GPIO_NOT_EXISTING:    "GPIO not existing",
    VL53L0X_ERROR_GPIO_FUNCTIONALITY_NOT_SUPPORTED: "GPIO funct not supported",
    VL53L0X_ERROR_INTERRUPT_NOT_CLEARED:"Interrupt not Cleared",
    VL53L0X_ERROR_CONTROL_INTERFACE:    "Control Interface Error",
    VL53L0X_ERROR_INVALID_COMMAND:      "Invalid Command Error",
    VL53L0X_ERROR_DIVISION_BY_ZERO:     "Division by zero Error",
    VL53L0X_ERROR_REF_SPAD_INIT:        "Reference Spad Init Error",
    VL53L0X_ERROR_NOT_IMPLEMENTED:      "Not implemented error"
}



def get_pal_error_string(PalErrorCode, PalErrorString:ErrorString):
    status = VL53L0X_ERROR_NONE

    try:
        PalErrorString.err_str = ErrorStringDict[PalErrorCode]
    except KeyError:
        PalErrorString.err_str = STRING_UNKNOW_ERROR_CODE
    
    return status