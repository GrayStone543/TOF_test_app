#include <stdio.h>
#include <stdlib.h>

#include "vl53l0x_api.h"
#include "vl53l0x_platform.h"



#define STATUS_OK           0
#define STATUS_FAIL         1


int VL53L0X_i2c_init(void);

int init_done = 0;
VL53L0X_Dev_t Dev;
VL53L0X_DeviceInfo_t DeviceInfo;
VL53L0X_RangingMeasurementData_t RangingMeasurementData;
char range_status_buf[64];


int VL53L0X_open()
{
    int status;

    uint32_t refSpadCount;
    uint8_t isApertureSpads;
    uint8_t VhvSettings;
    uint8_t PhaseCal;

    Dev.I2cDevAddr = 0x52;

    status = VL53L0X_i2c_init();
    if (status == VL53L0X_ERROR_NONE) {
        init_done = 1;

        // VL53L0X_GetVersion(&Version);

        status = VL53L0X_DataInit(&Dev); // Data initialization
        if (status == VL53L0X_ERROR_NONE) {
            status = VL53L0X_GetDeviceInfo(&Dev, &DeviceInfo);
            if (status == VL53L0X_ERROR_NONE) {
                // printf("VL53L0X_GetDeviceInfo:\n");
                // printf("Device Name : %s\n", DeviceInfo.Name);
                // printf("Device Type : %s\n", DeviceInfo.Type);
                // printf("Device ID : %s\n", DeviceInfo.ProductId);
                // printf("ProductRevisionMajor : %d\n", DeviceInfo.ProductRevisionMajor);
                // printf("ProductRevisionMinor : %d\n", DeviceInfo.ProductRevisionMinor);

                if ((DeviceInfo.ProductRevisionMinor != 1) && (DeviceInfo.ProductRevisionMinor != 1)) {
                    printf("Error expected cut 1.1 but found cut %d.%d\n", DeviceInfo.ProductRevisionMajor, DeviceInfo.ProductRevisionMinor);
                    status = VL53L0X_ERROR_NOT_SUPPORTED;
                }
            }
        }
    }

    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_StaticInit(&Dev);
    }

    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_PerformRefCalibration(&Dev, &VhvSettings, &PhaseCal);
    }
    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_PerformRefSpadManagement(&Dev, &refSpadCount, &isApertureSpads);
    }

    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_SetDeviceMode(&Dev, VL53L0X_DEVICEMODE_SINGLE_RANGING);
    }

    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_SetLimitCheckEnable(&Dev, VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE, 1);
    }
    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_SetLimitCheckEnable(&Dev, VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE, 1);
    }
    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_SetLimitCheckEnable(&Dev, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, 1);
    }
    if (status == VL53L0X_ERROR_NONE) {
        status = VL53L0X_SetLimitCheckValue(&Dev, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, (FixPoint1616_t)(1.5*0.023*65536));
    }

    return status;
}


int VL53L0X_close()
{
    int status = VL53L0X_ERROR_NONE;

    if (init_done != 0) {
        VL53L0X_comms_close();
    }

    return status;
}


int VL53L0X_perform_ranging_measurement()
{
    int status;

    status = VL53L0X_PerformSingleRangingMeasurement(&Dev, &RangingMeasurementData);

    return status;
}


int VL53L0X_get_range_millimeter()
{
    return RangingMeasurementData.RangeMilliMeter;
}


int VL53L0X_get_range_status()
{
    return RangingMeasurementData.RangeStatus;
}


char *VL53L0X_get_range_status_str()
{
    char buf[VL53L0X_MAX_STRING_LENGTH];

    /*
     * New Range Status: data is valid when pRangingMeasurementData->RangeStatus = 0
     */
    VL53L0X_GetRangeStatusString(RangingMeasurementData.RangeStatus, buf);
    // printf("Range Status: %i : %s\n", RangingMeasurementData.RangeStatus, buf);
    snprintf(range_status_buf, 64, "Range Status: %i : %s", RangingMeasurementData.RangeStatus, buf);

    return range_status_buf;
}


float VL53L0X_get_limit()
{
    FixPoint1616_t LimitCheckCurrent;
    float f_limit;

    VL53L0X_GetLimitCheckCurrent(&Dev, VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD, &LimitCheckCurrent);
    // printf("RANGE IGNORE THRESHOLD: %f\n\n", (float)LimitCheckCurrent/65536.0);
    f_limit = (float)LimitCheckCurrent/65536.0;

    return f_limit;
}