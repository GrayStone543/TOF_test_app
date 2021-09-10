from .defines import *
from .api_strings import get_pal_error_string
from .platform import *


def VL53L0X_GetPalErrorString(PalErrorCode, PalErrorString:ErrorString):
    status = ERROR_NONE

    status = get_pal_error_string(PalErrorCode, PalErrorString)
    return status


def VL53L0X_StaticInit(Dev):
    status = ERROR_NONE

    status = VL53L0X_get_info_from_device(Dev, 1)

    # set the ref spad from NVM
    count = PALDevDataGet(Dev, "ReferenceSpadCount")
    ApertureSpads = PALDevDataGet(Dev, "ReferenceSpadType")

    if ApertureSpads > 1 or (ApertureSpads == 1 and count > 32) or (ApertureSpads == 0 and count > 12):
        status = VL53L0X_perform_ref_spad_management(Dev, refSpadCount, isApertureSpads)
    else:
        status = VL53L0X_set_reference_spads(Dev, count, ApertureSpads)
    
    # initialize tuning settings buffer to prevent compiler warning
    pTuningSettingBuffer = DefaultTuningSettings

    if status == ERROR_NONE:
        UseInternalTuningSettings = PALDevDataGet(Dev, "UseInternalTuningSettings")

        if UseInternalTuningSettings == 0:
            pTuningSettingBuffer = PALDevDataGet(Dev, "pTuningSettingsPointer")
        else:
            pTuningSettingBuffer = DefaultTuningSettings
    
    if status == ERROR_NONE:
        status = VL53L0X_load_tuning_settings(Dev, pTuningSettingBuffer)
    
    # Set interrupt config to new sample ready
    if status == ERROR_NONE:
        status = VL53L0X_GetGpioConfig(Dev, 0, 0, VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_NEW_SAMPLE_READY, VL53L0X_INTERRUPTPOLARITY_LOW)
    
    if status == ERROR_NONE:
        tempword = []
        status = VL53L0X_WrByte(Dev, 0xFF, [0x01])
        status = status | VL53L0X_RdWord(Dev, 0x84, tempword)
        status = status | VL53L0X_WrByte(Dev, 0xFF, [0x00])
    
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "OscFrequencyMHz", VL53L0X_FIXPOINT412TOFIXPOINT1616(tempword[0]))
    
    # After static init, some device parameters may be changed,
    # so update them
    if status == ERROR_NONE:
        status = VL53L0X_GetDeviceParameters(Dev, CurrentParameters)
    
    if status == ERROR_NONE:
        tempbyte = []
        status = VL53L0X_GetFractionEnable(Dev, tempbyte)
        if status == ERROR_NONE:
            PALDevDataSet(Dev, "RangeFractionalEnable", tempbyte[0])
    
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "CurrentParameters", CurrentParameters)
    
    # read the sequence config and save it
    if status == ERROR_NONE:
        status = VL53L0X_RdByte(Dev, VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG, tempbyte)
        if status == ERROR_NONE:
            PALDevDataSet(Dev, "SequenceConfig", tempbyte[0])
    
    # Disable MSRC and TCC by default
    if status == ERROR_NONE:
        status = VL53L0X_SetSequenceStepEnable(Dev, VL53L0X_SEQUENCESTEP_TCC, 0)
    
    if status == ERROR_NONE:
        status = VL53L0X_SetSequenceStepEnable(Dev, VL53L0X_SEQUENCESTEP_MSRC, 0)
    
    # set PAL State to standby
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "PalState", STATE_IDLE)
    
    # Store pre-range vcsel period
    if status == ERROR_NONE:
        status = VL53L0X_GetVcselPulsePeriod(Dev, VL53L0X_VCSEL_PERIOD_PRE_RANGE, vcselPulsePeriodPCLK)
    
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "PreRangeVcselPulsePeriod", vcselPulsePeriodPCLK)
    
    # Store final-range vcsel period
    if status == ERROR_NONE:
        status = VL53L0X_GetVcselPulsePeriod(Dev, VL53L0X_VCSEL_PERIOD_FINAL_RANGE, vcselPulsePeriodPCLK)
    
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "FinalRangeVcselPulsePeriod", vcselPulsePeriodPCLK)
    
    # Store pre-range timeout
    if status == ERROR_NONE:
        status = get_sequence_step_timeout(Dev, VL53L0X_SEQUENCESTEP_PRE_RANGE, seqTimeoutMicroSecs)
    
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "PreRangeTimeoutMicroSecs", seqTimeoutMicroSecs)
    
    # Store final-range timeout
    if status == ERROR_NONE:
        status = get_sequence_step_timeout(Dev, VL53L0X_SEQUENCESTEP_FINAL_RANGE, seqTimeoutMicroSecs)
    
    if status == ERROR_NONE:
        PALDevDataSet(Dev, "FinalRangeTimeoutMicroSecs", seqTimeoutMicroSecs)
    
    return status