


VL53L0X_DEFAULT_MAX_LOOP                        = 2000

VL53L0X_REF_SPAD_BUFFER_SIZE                    = 6


# Error and Warning code returned by API
VL53L0X_ERROR_NONE                              = 0
VL53L0X_ERROR_CALIBRATION_WARNING               = -1
VL53L0X_ERROR_MIN_CLIPPED                       = -2
VL53L0X_ERROR_UNDEFINED                         = -3
VL53L0X_ERROR_INVALID_PARAMS                    = -4
VL53L0X_ERROR_NOT_SUPPORTED                     = -5
VL53L0X_ERROR_RANGE_ERROR                       = -6
VL53L0X_ERROR_TIME_OUT                          = -7
VL53L0X_ERROR_MODE_NOT_SUPPORTED                = -8
VL53L0X_ERROR_BUFFER_TOO_SMALL                  = -9
VL53L0X_ERROR_GPIO_NOT_EXISTING                 = -10
VL53L0X_ERROR_GPIO_FUNCTIONALITY_NOT_SUPPORTED  = -11
VL53L0X_ERROR_INTERRUPT_NOT_CLEARED             = -12
VL53L0X_ERROR_CONTROL_INTERFACE                 = -20
VL53L0X_ERROR_INVALID_COMMAND                   = -30
VL53L0X_ERROR_DIVISION_BY_ZERO                  = -40
VL53L0X_ERROR_REF_SPAD_INIT                     = -50
VL53L0X_ERROR_NOT_IMPLEMENTED                   = -99


# Defines Device modes
VL53L0X_DEVICEMODE_SINGLE_RANGING               = 0
VL53L0X_DEVICEMODE_CONTINUOUS_RANGING           = 1
VL53L0X_DEVICEMODE_SINGLE_HISTOGRAM             = 2
VL53L0X_DEVICEMODE_CONTINUOUS_TIMED_RANGING     = 3
VL53L0X_DEVICEMODE_SINGLE_ALS                   = 10
VL53L0X_DEVICEMODE_GPIO_DRIVE                   = 20
VL53L0X_DEVICEMODE_GPIO_OSC                     = 21


# Defines Histogram modes
VL53L0X_HISTOGRAMMODE_DISABLE                   = 0
VL53L0X_HISTOGRAMMODE_REFERENCE_ONLY            = 1
VL53L0X_HISTOGRAMMODE_RETURN_ONLY               = 2
VL53L0X_HISTOGRAMMODE_BOTH                      = 3


# List of available Power Modes
VL53L0X_POWERMODE_STANDBY_LEVEL1                = 0
VL53L0X_POWERMODE_STANDBY_LEVEL2                = 1
VL53L0X_POWERMODE_IDLE_LEVEL1                   = 2
VL53L0X_POWERMODE_IDLE_LEVEL2                   = 3


# Defines the current status
VL53L0X_STATE_POWERDOWN                         = 0
VL53L0X_STATE_WAIT_STATICINIT                   = 1
VL53L0X_STATE_STANDBY                           = 2
VL53L0X_STATE_IDLE                              = 3
VL53L0X_STATE_RUNNING                           = 4
VL53L0X_STATE_UNKNOW                            = 98
VL53L0X_STATE_ERROR                             = 99


# Defines the Polarity of the Interrupt
VL53L0X_INTERRUPTPOLARITY_LOW                   = 0
VL53L0X_INTERRUPTPOLARITY_HIGH                  = 1


# Defines the range measurement for which to access the vcsel period.
VL53L0X_VCSEL_PERIOD_PRE_RANGE                  = 0
VL53L0X_VCSEL_PERIOD_FINAL_RANGE                = 1


# Defines the sequence steps performed during ranging.
VL53L0X_SEQUENCESTEP_TCC                        = 0
VL53L0X_SEQUENCESTEP_DSS                        = 1
VL53L0X_SEQUENCESTEP_MSRC                       = 2
VL53L0X_SEQUENCESTEP_PRE_RANGE                  = 3
VL53L0X_SEQUENCESTEP_FINAL_RANGE                = 4
VL53L0X_SEQUENCESTEP_NUMBER_OF_CHECKS           = 5


def VL53L0X_FIXPOINT1616TOFIXPOINT412(Value):
    return (Value>>4)&0xffff


def VL53L0X_FIXPOINT412TOFIXPOINT1616(Value):
    return (Value << 4)


def VL53L0X_FIXPOINT1616TOFIXPOINT97(Value):
    return ((Value >> 9) & 0xffff)

def VL53L0X_FIXPOINT97TOFIXPOINT1616(Value):
    return (Value << 9)


class ErrorString:
    def __init__(self):
        self.err_str = ""
    
    def __repr__(self):
        return self.err_str


class VL53L0X_Device:
    def __init__(self):
        self.I2cDevAddr = 0x52
        self.Data = dict(
                ReadDataFromDeviceDone=int(0),
                ReferenceSpadCount=int(0),
                ReferenceSpadType=int(0),
                targetRefRate = int(0)
                )
        self.SpadData = dict(
            RefSpadEnables=[0 for i in range(VL53L0X_REF_SPAD_BUFFER_SIZE)],
            RefGoodSpadMap=[0 for i in range(VL53L0X_REF_SPAD_BUFFER_SIZE)])
    
    def __repr__(self):
        return self.Data.__repr__()


class IntData:
    def __init__(self, init_value:int=0):
        self.value = init_value
    
    def __repr__(self):
        return "0x{:X}".format(self.value)
    
    def bitAND(self, mask:int):
        return int(self.value & mask)
    
    def bitOR(self, mask:int):
        return int(self.value | mask)
    
    def bitRShift(self, num_of_bits:int):
        return int(self.value >> num_of_bits)
    
    def bitLShift(self, num_of_bits:int):
        return int(self.value << num_of_bits)
    
