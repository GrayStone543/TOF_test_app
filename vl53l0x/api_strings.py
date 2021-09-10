from defines import *


STRING_UNKNOW_ERROR_CODE            = "Unknow Error Code"

ErrorStringDict = {
    ERROR_NONE:                 "No Error",
    ERROR_CALIBRATION_WARNING:  "Calibration Warning Error",
    ERROR_MIN_CLIPPED:          "Min clipped error",
    ERROR_UNDEFINED:            "Undefined error",
    ERROR_INVALID_PARAMS:       "Invalid parameters error",
    ERROR_NOT_SUPPORTED:        "Not supported error",
    ERROR_RANGE_ERROR:          "Range error",
    ERROR_TIME_OUT:             "Time out error",
    ERROR_MODE_NOT_SUPPORTED:   "Mode not supported error",
    ERROR_BUFFER_TOO_SMALL:     "Buffer too small",
    ERROR_GPIO_NOT_EXISTING:    "GPIO not existing",
    ERROR_GPIO_FUNCTIONALITY_NOT_SUPPORTED: "GPIO funct not supported",
    ERROR_INTERRUPT_NOT_CLEARED:"Interrupt not Cleared",
    ERROR_CONTROL_INTERFACE:    "Control Interface Error",
    ERROR_INVALID_COMMAND:      "Invalid Command Error",
    ERROR_DIVISION_BY_ZERO:     "Division by zero Error",
    ERROR_REF_SPAD_INIT:        "Reference Spad Init Error",
    ERROR_NOT_IMPLEMENTED:      "Not implemented error"
}



def get_pal_error_string(PalErrorCode, PalErrorString:ErrorString):
    status = ERROR_NONE

    try:
        PalErrorString.err_str = ErrorStringDict[PalErrorCode]
    except KeyError:
        PalErrorString.err_str = STRING_UNKNOW_ERROR_CODE
    
    return status