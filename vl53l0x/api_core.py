from vl53l0x.platform import PALDevDataGet
from .defines import *
from .platform import PALDevDataSet, VL53L0X_RdByte, VL53L0X_RdDWord, VL53L0X_WrByte, VL53L0X_PollingDelay, VL53L0X_read_dword


def VL53L0X_device_read_strobe(Dev:VL53L0X_Device):
    Status = VL53L0X_ERROR_NONE

    Status |= VL53L0X_WrByte(Dev, 0x83, 0x00)

    # polling
    # use timeout to avoid deadlock

    if Status == VL53L0X_ERROR_NONE:
        LoopNb = 0
        condition = True
        strobe = IntData()
        while condition:
            Status = VL53L0X_RdByte(Dev, 0x83, strobe)
            if strobe.value != 0x00 or Status != VL53L0X_ERROR_NONE:
                break
            LoopNb = LoopNb + 1
            condition = (LoopNb < VL53L0X_DEFAULT_MAX_LOOP)
        
        if LoopNb >= VL53L0X_DEFAULT_MAX_LOOP:
            Status = VL53L0X_ERROR_TIME_OUT
    
    Status |= VL53L0X_WrByte(Dev, 0x83, 0x01)

    return Status


def VL53L0X_get_info_from_device(Dev:VL53L0X_Device, option):
    Status = 0
    ReferenceSpadCount = 0
    ReferenceSpadType = 0
    PartUIDUpper = IntData()
    PartUIDLower = IntData()
    OffsetFixed1104_mm = 0
    OffsetMicroMeters = 0
    DistMeasTgtFixed1104_mm = 400 << 4
    DistMeasFixed1104_400_mm = 0
    SignalRateMeasFixed1104_400_mm = 0
    SignalRateMeasFixed400mmFix = 0
    tmpByte = IntData()
    TmpDWord = IntData()
    NvmRefGoodSpadMap = [0 for i in range(VL53L0X_REF_SPAD_BUFFER_SIZE)]
    ModuleId = IntData()
    Revision = IntData()
    ProductId = ""

    ReadDataFromDeviceDone = PALDevDataGet(Dev, "ReadDataFromDeviceDone")

    # This access is done only once after that a GetDeviceInfo or
    # datainit is done
    if ReadDataFromDeviceDone != 7:

        Status |= VL53L0X_WrByte(Dev, 0x80, 0x01)
        Status |= VL53L0X_WrByte(Dev, 0xFF, 0x01)
        Status |= VL53L0X_WrByte(Dev, 0x00, 0x00)

        Status |= VL53L0X_WrByte(Dev, 0xFF, 0x06)
        Status |= VL53L0X_RdByte(Dev, 0x83, tmpByte)
        Status |= VL53L0X_WrByte(Dev, 0x83, tmpByte.bitOR(4))
        Status |= VL53L0X_WrByte(Dev, 0xFF, 0x07)
        Status |= VL53L0X_WrByte(Dev, 0x81, 0x01)

        Status |= VL53L0X_PollingDelay(Dev)

        Status |= VL53L0X_WrByte(Dev, 0x80, 0x01)

        if (option & 1) == 1 and (ReadDataFromDeviceDone & 1) == 0:
            Status |= VL53L0X_WrByte(Dev, 0x94, 0x6b)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            ReferenceSpadCount = TmpDWord.bitRShift(8) & 0x07f
            ReferenceSpadType = TmpDWord.bitRShift(15) & 0x01

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x24)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            NvmRefGoodSpadMap[0] = TmpDWord.bitRShift(24) & 0xff
            NvmRefGoodSpadMap[1] = TmpDWord.bitRShift(16) & 0xff
            NvmRefGoodSpadMap[2] = TmpDWord.bitRShift(8) & 0xff
            NvmRefGoodSpadMap[3] = (TmpDWord.value & 0xff)

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x25)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            NvmRefGoodSpadMap[4] = TmpDWord.bitRShift(24) & 0xff
            NvmRefGoodSpadMap[5] = TmpDWord.bitRShift(16) & 0xff
        
        if (option & 2) == 2 and (ReadDataFromDeviceDone & 2) == 0:
            Status |= VL53L0X_WrByte(Dev, 0x94, 0x02)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdByte(Dev, 0x90, ModuleId)

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x7B)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdByte(Dev, 0x90, Revision)

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x77)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            ProductId += chr(TmpDWord.bitRShift(25) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(18) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(11) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(4) & 0x07f)

            byte = TmpDWord.bitAND(0x00f) << 3

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x78)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            ProductId += chr(byte + (TmpDWord.bitRShift(29) & 0x07f))
            ProductId += chr(TmpDWord.bitRShift(22) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(15) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(8) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(1) & 0x07f)

            byte = TmpDWord.bitAND(0x001) << 6

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x79)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            ProductId += chr(byte + (TmpDWord.bitRshift(26) & 0x07f))
            ProductId += chr(TmpDWord.bitRShift(19) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(12) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(5) & 0x07f)

            byte = TmpDWord.bitAND(0x01f) << 2

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x7A)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            ProductId += chr(byte + (TmpDWord.bitRShift(30) & 0x07f))
            ProductId += chr(TmpDWord.bitRShift(23) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(16) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(9) & 0x07f)
            ProductId += chr(TmpDWord.bitRShift(2) & 0x07f)
            # ProductId[18] = '\0'
        
        if (option & 4) == 4 and (ReadDataFromDeviceDone & 4) == 0:
            Status |= VL53L0X_WrByte(Dev, 0x94, 0x7B)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, PartUIDUpper)

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x7C)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, PartUIDLower)

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x73)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            SignalRateMeasFixed1104_400_mm = TmpDWord.bitAND(0x000000ff) << 8

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x74)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            SignalRateMeasFixed1104_400_mm |= (TmpDWord.bitAND(0xff000000) >> 24)

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x75)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            DistMeasFixed1104_400_mm = TmpDWord.bitAND(0x000000ff) << 8

            Status |= VL53L0X_WrByte(Dev, 0x94, 0x76)
            Status |= VL53L0X_device_read_strobe(Dev)
            Status |= VL53L0X_RdDWord(Dev, 0x90, TmpDWord)

            DistMeasFixed1104_400_mm |= (TmpDWord.bitAND(0xff000000) >> 24)
        
        Status |= VL53L0X_WrByte(Dev, 0x81, 0x00)
        Status |= VL53L0X_WrByte(Dev, 0xFF, 0x06)
        Status |= VL53L0X_RdByte(Dev, 0x83, tmpByte)
        Status |= VL53L0X_WrByte(Dev, 0x83, tmpByte.bitAND(0xfb))
        Status |= VL53L0X_WrByte(Dev, 0xFF, 0x01)
        Status |= VL53L0X_WrByte(Dev, 0x00, 0x01)

        Status |= VL53L0X_WrByte(Dev, 0xFF, 0x00)
        Status |= VL53L0X_WrByte(Dev, 0x80, 0x00)
    
    if Status == VL53L0X_ERROR_NONE and ReadDataFromDeviceDone != 7:
        # Assign to variable if status is ok
        if (option & 1) == 1 and (ReadDataFromDeviceDone & 1) == 0:
            PALDevDataSet(Dev, "ReferenceSpadCount", ReferenceSpadCount)
            PALDevDataSet(Dev, "ReferenceSpadType", ReferenceSpadType)
            for i in range(VL53L0X_REF_SPAD_BUFFER_SIZE):
                Dev.SpadData["RefGoodSpadMap"][i] = NvmRefGoodSpadMap[i]
        
        if (option & 2) == 2 and (ReadDataFromDeviceDone & 2) == 0:
            PALDevDataSet(Dev, "ModuleId", ModuleId.value)
            PALDevDataSet(Dev, "Revision", Revision.value)
            PALDevDataSet(Dev, "ProductId", ProductId)
        
        if (option & 4) == 4 and (ReadDataFromDeviceDone & 4) == 0:
            PALDevDataSet(Dev, "PartUIDUpper", PartUIDUpper.value)
            PALDevDataSet(Dev, "PartUIDLower", PartUIDLower.value)

            SignalRateMeasFixed400mmFix = VL53L0X_FIXPOINT97TOFIXPOINT1616(SignalRateMeasFixed1104_400_mm)
            PALDevDataSet(Dev, "SignalRateMeasFixed400mm", SignalRateMeasFixed400mmFix)

            OffsetMicroMeters = 0
            if DistMeasFixed1104_400_mm != 0:
                OffsetFixed1104_mm = DistMeasFixed1104_400_mm - DistMeasTgtFixed1104_mm
                OffsetMicroMeters = (OffsetFixed1104_mm * 1000) >> 4
                OffsetMicroMeters = OffsetMicroMeters * (-1)
            PALDevDataSet(Dev, "Part2PartOffsetAdjustmentNVMMicroMeter", OffsetMicroMeters)
        byte = ReadDataFromDeviceDone | option
        PALDevDataSet(Dev, "ReadDataFromDeviceDone", byte)
    
    return Status