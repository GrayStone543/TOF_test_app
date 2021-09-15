from vl53l0x.platform import PALDevDataGet, VL53L0X_WrByte
from .defines import *
from .device import *


def VL53L0X_perform_ref_spad_management(Dev:VL53L0X_Device, refSpadCount, isApertureSpads:IntData):
    Status = VL53L0X_ERROR_NONE
    lastSpadArray = [0 for i in range(VL53L0X_REF_SPAD_BUFFER_SIZE)]
    startSelect = 0xB4
    minimumSpadCount = 3
    maxSpadCount = 44
    currentSpadIndex = 0
    lastSpadIndex = 0
    nextGoodSpad = 0
    targetRefRate = 0x0A00
    peakSignalRateRef = 0
    needAptSpads = 0
    index = 0
    spadArraySize = VL53L0X_REF_SPAD_BUFFER_SIZE
    signalRateDiff = 0
    lastSignalRateDiff = 0
    complete = 0
    VhvSettings = 0
    PhaseCal = 0
    refSpadCount_int = 0
    isApertureSpads_int = 0

    targetRefRate = PALDevDataGet(Dev, "targetRefRate")

    # Initialize Spad arrays.
    # Currently the good spad map is initialised to 'All good'.
    # This is a short term implementation. The good spad map will be
    # provided as an input.
    # Note that there are 6 bytes. Only the first 44 bits will be used to
    # represent spads.
    for i in range(spadArraySize):
        Dev.SpadData["RefSpadEnables"][i] = 0

    Status = VL53L0X_WrByte(Dev, 0xFF, 0x01)

    if Status == VL53L0X_ERROR_NONE:
        Status = VL53L0X_WrByte(Dev, VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET, 0x00)
    
    if Status == VL53L0X_ERROR_NONE:
        Status = VL53L0X_WrByte(Dev, VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD, 0x2C)
    
    if Status == VL53L0X_ERROR_NONE:
        Status = VL53L0X_WrByte(Dev, 0xFF, 0x00)
    
    if Status == VL53L0X_ERROR_NONE:
        Status = VL53L0X_WrByte(Dev, VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT, startSelect)
    

    if Status == VL53L0X_ERROR_NONE:
        Status = VL53L0X_WrByte(Dev, VL53L0X_REG_POWER_MANAGEMENT_GO1_POWER_FORCE, 0)
    
    # Perform ref calibration