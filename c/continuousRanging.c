#include "vl53l0x_api.h"
#include "vl53l0x_platform.h"
#include <malloc.h>

#include "utils.h"



VL53L0X_Error WaitMeasurementDataReady(VL53L0X_DEV Dev)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    uint8_t NewDatReady = 0;
    uint32_t LoopNb;

    // Wait until it finished
    // use timeout to avoid deadlock
    if (Status == VL53L0X_ERROR_NONE) {
        LoopNb = 0;
        do {
            Status = VL53L0X_GetMeasurementDataReady(Dev, &NewDatReady);
            if ((NewDatReady == 0x01) || Status != VL53L0X_ERROR_NONE) {
                break;
            }
            LoopNb = LoopNb + 1;
            VL53L0X_PollingDelay(Dev);
        } while (LoopNb < VL53L0X_DEFAULT_MAX_LOOP);

        if (LoopNb >= VL53L0X_DEFAULT_MAX_LOOP) {
            Status = VL53L0X_ERROR_TIME_OUT;
        }
    }

    return Status;
}

VL53L0X_Error WaitStopCompleted(VL53L0X_DEV Dev)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    uint32_t StopCompleted = 0;
    uint32_t LoopNb;

    // Wait until it finished
    // use timeout to avoid deadlock
    if (Status == VL53L0X_ERROR_NONE) {
        LoopNb = 0;
        do {
            Status = VL53L0X_GetStopCompletedStatus(Dev, &StopCompleted);
            if ((StopCompleted == 0x00) || Status != VL53L0X_ERROR_NONE) {
                break;
            }
            LoopNb = LoopNb + 1;
            VL53L0X_PollingDelay(Dev);
        } while (LoopNb < VL53L0X_DEFAULT_MAX_LOOP);

        if (LoopNb >= VL53L0X_DEFAULT_MAX_LOOP) {
            Status = VL53L0X_ERROR_TIME_OUT;
        }

    }

    return Status;
}
    
    
VL53L0X_Error continuous_rangingTest(VL53L0X_Dev_t *pMyDevice)
{
    VL53L0X_RangingMeasurementData_t    RangingMeasurementData;
    VL53L0X_RangingMeasurementData_t   *pRangingMeasurementData    = &RangingMeasurementData;
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    uint32_t refSpadCount;
    uint8_t isApertureSpads;
    uint8_t VhvSettings;
    uint8_t PhaseCal;

    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_StaticInit\n");
        Status = VL53L0X_StaticInit(pMyDevice); // Device Initialization
        // StaticInit will set interrupt by default
        print_pal_error(Status);
    }
    
    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_PerformRefCalibration\n");
        Status = VL53L0X_PerformRefCalibration(pMyDevice, &VhvSettings, &PhaseCal); // Device Initialization
        print_pal_error(Status);
    }

    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_PerformRefSpadManagement\n");
        Status = VL53L0X_PerformRefSpadManagement(pMyDevice, &refSpadCount, &isApertureSpads); // Device Initialization
        print_pal_error(Status);
    }

    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_SetDeviceMode\n");
        Status = VL53L0X_SetDeviceMode(pMyDevice, VL53L0X_DEVICEMODE_CONTINUOUS_RANGING);
        print_pal_error(Status);
    }
    
    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_StartMeasurement\n");
        Status = VL53L0X_StartMeasurement(pMyDevice);
        print_pal_error(Status);
    }

    if (Status == VL53L0X_ERROR_NONE) {
        uint32_t measurement;
        uint32_t no_of_measurements = 32;

        uint16_t* pResults = (uint16_t*)malloc(sizeof(uint16_t) * no_of_measurements);

        for (measurement=0; measurement<no_of_measurements; measurement++) {

            Status = WaitMeasurementDataReady(pMyDevice);

            if (Status == VL53L0X_ERROR_NONE) {
                Status = VL53L0X_GetRangingMeasurementData(pMyDevice, pRangingMeasurementData);

                *(pResults + measurement) = pRangingMeasurementData->RangeMilliMeter;
                printf("In loop measurement %d: %d mm\n", measurement, pRangingMeasurementData->RangeMilliMeter);

                // Clear the interrupt
                VL53L0X_ClearInterruptMask(pMyDevice, VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_NEW_SAMPLE_READY);
                VL53L0X_PollingDelay(pMyDevice);
            }
            else {
                break;
            }
        }

        if (Status == VL53L0X_ERROR_NONE) {
            for(measurement=0; measurement<no_of_measurements; measurement++) {
                printf("measurement %d: %d mm\n", measurement, *(pResults + measurement));
            }
        }

        free(pResults);
    }

    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_StopMeasurement\n");
        Status = VL53L0X_StopMeasurement(pMyDevice);
    }

    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Wait Stop to be competed\n");
        Status = WaitStopCompleted(pMyDevice);
    }

    if (Status == VL53L0X_ERROR_NONE)
        Status = VL53L0X_ClearInterruptMask(pMyDevice, VL53L0X_REG_SYSTEM_INTERRUPT_GPIO_NEW_SAMPLE_READY);

    return Status;
}


int continuous_ranging(void)
{
    VL53L0X_Error Status = VL53L0X_ERROR_NONE;
    VL53L0X_Dev_t MyDevice;
    VL53L0X_Dev_t *pMyDevice = &MyDevice;
    VL53L0X_Version_t                   Version;
    VL53L0X_Version_t                  *pVersion   = &Version;
    VL53L0X_DeviceInfo_t                DeviceInfo;

    int32_t status_int;
    int32_t init_done = 0;


    printf ("VL53L0X PAL Continuous Ranging example\n\n");
//    printf ("Press a Key to continue!");
//    getchar();

    // Initialize Comms
    pMyDevice->I2cDevAddr      = 0x52;
    pMyDevice->comms_type      =  1;
    pMyDevice->comms_speed_khz =  400;

    Status = VL53L0X_i2c_init();
    if (Status != VL53L0X_ERROR_NONE) {
        Status = VL53L0X_ERROR_CONTROL_INTERFACE;
        init_done = 1;
    }
    else
        printf ("Init Comms\n");

    /*
     * Disable VL53L0X API logging if you want to run at full speed
     */
#ifdef VL53L0X_LOG_ENABLE
    VL53L0X_trace_config("test.log", TRACE_MODULE_ALL, TRACE_LEVEL_ALL, TRACE_FUNCTION_ALL);
#endif

    /*
     *  Get the version of the VL53L0X API running in the firmware
     */

    if (Status == VL53L0X_ERROR_NONE) {
        status_int = VL53L0X_GetVersion(pVersion);
        if (status_int != 0)
            Status = VL53L0X_ERROR_CONTROL_INTERFACE;
    }

    /*
     *  Verify the version of the VL53L0X API running in the firmrware
     */
    if (Status == VL53L0X_ERROR_NONE) {
        printf("VL53L0X API Version: %d.%d.%d (revision %d)\n", pVersion->major, pVersion->minor, pVersion->build, pVersion->revision);
    }

    // End of implementation specific
    if (Status == VL53L0X_ERROR_NONE) {
        printf ("Call of VL53L0X_DataInit\n");
        Status = VL53L0X_DataInit(&MyDevice); // Data initialization
        print_pal_error(Status);
    }
    
    if (Status == VL53L0X_ERROR_NONE) {
        Status = VL53L0X_GetDeviceInfo(&MyDevice, &DeviceInfo);
    }
    if (Status == VL53L0X_ERROR_NONE) {
        printf("VL53L0X_GetDeviceInfo:\n");
        printf("Device Name : %s\n", DeviceInfo.Name);
        printf("Device Type : %s\n", DeviceInfo.Type);
        printf("Device ID : %s\n", DeviceInfo.ProductId);
        printf("ProductRevisionMajor : %d\n", DeviceInfo.ProductRevisionMajor);
        printf("ProductRevisionMinor : %d\n", DeviceInfo.ProductRevisionMinor);

        if ((DeviceInfo.ProductRevisionMinor != 1) && (DeviceInfo.ProductRevisionMinor != 1)) {
        	printf("Error expected cut 1.1 but found cut %d.%d\n",
        			DeviceInfo.ProductRevisionMajor, DeviceInfo.ProductRevisionMinor);
        	Status = VL53L0X_ERROR_NOT_SUPPORTED;
        }
    }
    
    if(Status == VL53L0X_ERROR_NONE)
    {
        Status = continuous_rangingTest(pMyDevice);
    }

    print_pal_error(Status);
    
    // Implementation specific
    /*
     *  Disconnect comms - part of VL53L0X_platform.c
     */

    if(init_done == 0) {
        printf ("Close Comms\n");
        status_int = VL53L0X_comms_close();
        if (status_int != 0)
            Status = VL53L0X_ERROR_CONTROL_INTERFACE;
    }

    print_pal_error(Status);
    // End of implementation specific
    
//    printf ("Press a Key to continue!");
//    getchar();
    
    return (0);
}

