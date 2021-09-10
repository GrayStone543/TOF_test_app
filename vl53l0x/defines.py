

# Error and Warning code returned by API
ERROR_NONE                              = 0
ERROR_CALIBRATION_WARNING               = -1
ERROR_MIN_CLIPPED                       = -2
ERROR_UNDEFINED                         = -3
ERROR_INVALID_PARAMS                    = -4
ERROR_NOT_SUPPORTED                     = -5
ERROR_RANGE_ERROR                       = -6
ERROR_TIME_OUT                          = -7
ERROR_MODE_NOT_SUPPORTED                = -8
ERROR_BUFFER_TOO_SMALL                  = -9
ERROR_GPIO_NOT_EXISTING                 = -10
ERROR_GPIO_FUNCTIONALITY_NOT_SUPPORTED  = -11
ERROR_INTERRUPT_NOT_CLEARED             = -12
ERROR_CONTROL_INTERFACE                 = -20
ERROR_INVALID_COMMAND                   = -30
ERROR_DIVISION_BY_ZERO                  = -40
ERROR_REF_SPAD_INIT                     = -50
ERROR_NOT_IMPLEMENTED                   = -99


# Defines Device modes
DEVICEMODE_SINGLE_RANGING               = 0
DEVICEMODE_CONTINUOUS_RANGING           = 1
DEVICEMODE_SINGLE_HISTOGRAM             = 2
DEVICEMODE_CONTINUOUS_TIMED_RANGING     = 3
DEVICEMODE_SINGLE_ALS                   = 10
DEVICEMODE_GPIO_DRIVE                   = 20
DEVICEMODE_GPIO_OSC                     = 21


# Defines Histogram modes
HISTOGRAMMODE_DISABLE                   = 0
HISTOGRAMMODE_REFERENCE_ONLY            = 1
HISTOGRAMMODE_RETURN_ONLY               = 2
HISTOGRAMMODE_BOTH                      = 3


# List of available Power Modes
POWERMODE_STANDBY_LEVEL1                = 0
POWERMODE_STANDBY_LEVEL2                = 1
POWERMODE_IDLE_LEVEL1                   = 2
POWERMODE_IDLE_LEVEL2                   = 3


# Defines the current status
STATE_POWERDOWN                         = 0
STATE_WAIT_STATICINIT                   = 1
STATE_STANDBY                           = 2
STATE_IDLE                              = 3
STATE_RUNNING                           = 4
STATE_UNKNOW                            = 98
STATE_ERROR                             = 99


def VL53L0X_FIXPOINT1616TOFIXPOINT412(Value):
    return (Value>>4)&0xffff


def VL53L0X_FIXPOINT412TOFIXPOINT1616(Value):
    return (Value << 4)


class ErrorString:
    def __init__(self):
        self.err_str = ""
    
    def __repr__(self):
        return self.err_str


class VL53L0X_Device:
    def __init__(self):
        self.Data = dict()
        self.I2cDevAddr = 0x52
    
    def __repr__(self):
        return self.Data.__repr__()