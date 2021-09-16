#include <stdio.h>
#include <stdlib.h>

#include <linux/i2c.h>
#include <linux/i2c-dev.h>
// #include <i2c/smbus.h>
#include <fcntl.h> //define O_RDWR
#include <sys/ioctl.h>
#include <pthread.h>
#include <unistd.h>

#include "vl53l0x_i2c_platform.h"
#include "vl53l0x_def.h"
#include "vl53l0x_platform_log.h"

#ifdef VL53L0X_LOG_ENABLE
#define trace_print(level, ...) trace_print_module_function(TRACE_MODULE_PLATFORM, level, TRACE_FUNCTION_NONE, ##__VA_ARGS__)
#define trace_i2c(...) trace_print_module_function(TRACE_MODULE_NONE, TRACE_LEVEL_NONE, TRACE_FUNCTION_I2C, ##__VA_ARGS__)
#endif

// char  debug_string[VL53L0X_MAX_STRING_LENGTH_PLT];

uint8_t cached_page = 0;

#define MIN_COMMS_VERSION_MAJOR     1
#define MIN_COMMS_VERSION_MINOR     8
#define MIN_COMMS_VERSION_BUILD     1
#define MIN_COMMS_VERSION_REVISION  0


#define MAX_STR_SIZE 255
#define MAX_MSG_SIZE 100
#define MAX_DEVICES 4
#define STATUS_OK              0x00
#define STATUS_FAIL            0x01

pthread_mutex_t ghMutex;

// static unsigned char _dataBytes[MAX_MSG_SIZE];

typedef struct _devInfo {
    char devname[256];
    int fd;
    int address;
} DEV_INFO;

DEV_INFO gDevInfo;

bool_t _check_min_version(void)
{
    return 1;
}


int VL53L0X_i2c_init(void)
{
    strcpy(gDevInfo.devname, "/dev/i2c-8");
    gDevInfo.fd = -1;
    gDevInfo.address = 0x29;

    if (pthread_mutex_init(&ghMutex, NULL) != 0)
    {
        perror("\n mutex init failed\n");
        return STATUS_FAIL;
    }

    if ((gDevInfo.fd = open(gDevInfo.devname, O_RDWR)) < 0)
    {
        perror("Failed to open i2c device.\n");
        return STATUS_FAIL;
    }

    if (ioctl(gDevInfo.fd, I2C_SLAVE, gDevInfo.address) < 0)
    {
        printf("Failed to access bus.\n");
        return STATUS_FAIL;
    }

    // close(fd);

    return STATUS_OK;
}


int32_t VL53L0X_comms_close(void)
{
    pthread_mutex_destroy(&ghMutex);

    if (gDevInfo.fd > 0)
        close(gDevInfo.fd);

    return STATUS_OK;
}


int32_t VL53L0X_write_multi(uint8_t address, uint8_t reg, uint8_t *pdata, int32_t count)
{
    int32_t status = STATUS_OK;

    uint8_t *poutbuf;

    // unsigned int retries = 3;
    // uint8_t *pWriteData    = pdata;
    // uint8_t writeDataCount = count;
    // uint8_t writeReg       = reg;
    // DWORD dwWaitResult;

#ifdef VL53L0X_LOG_ENABLE
    int32_t i = 0;
    char value_as_str[VL53L0X_MAX_STRING_LENGTH_PLT];
    char *pvalue_as_str;
#endif

    /* For multi writes, the serial comms dll requires multiples 4 bytes or
     * anything less than 4 bytes. So if an irregular size is required, the
     * message is broken up into two writes.
     */
    // if((count > 4) && (count % 4 != 0))
    // {
    //     writeDataCount = 4*(count/4);
    //     status = VL53L0X_write_multi(address, writeReg, pWriteData, writeDataCount);

    //     if(status != STATUS_OK)
    //     {
    //         SERIAL_COMMS_Get_Error_Text(debug_string);
    //     }
    //     writeReg = reg + writeDataCount;
    //     pWriteData += writeDataCount;
    //     writeDataCount = count - writeDataCount;
    // }

#ifdef VL53L0X_LOG_ENABLE

    pvalue_as_str =  value_as_str;

    for(i = 0 ; i < count ; i++)
    {
        sprintf(pvalue_as_str,"%02X", *(pdata+i));

        pvalue_as_str += 2;
    }
    trace_i2c("Write reg : 0x%04X, Val : 0x%s\n", reg, value_as_str);
#endif

    struct i2c_rdwr_ioctl_data packets;
    struct i2c_msg messages[1];

    poutbuf = malloc(count+1);

    poutbuf[0] = reg;
    memcpy(&poutbuf[1], pdata, count);

    messages[0].addr    = gDevInfo.address;
    messages[0].flags   = 0;
    messages[0].len     = (unsigned short)(count + 1);
    messages[0].buf     = poutbuf;

    packets.msgs = messages;
    packets.nmsgs = 1;

    pthread_mutex_lock(&ghMutex);

    if (gDevInfo.fd > 0) {
        if (ioctl(gDevInfo.fd, I2C_RDWR, &packets) < 0) {
            status = STATUS_FAIL;
        }
    }
    else {
        status = STATUS_FAIL;
    }

    pthread_mutex_unlock(&ghMutex);

    // if(status == STATUS_OK)
    // {
    //     dwWaitResult = WaitForSingleObject(ghMutex, INFINITE);
    //     if(dwWaitResult == WAIT_OBJECT_0)
    //     {
    //         do
    //         {
    //             status = SERIAL_COMMS_Write_UBOOT(address, 0, writeReg, pWriteData, writeDataCount);
    //             // note : the field dwIndexHi is ignored. dwIndexLo will
    //             // contain the entire index (bits 0..15).
    //             if(status != STATUS_OK)
    //             {
    //                 SERIAL_COMMS_Get_Error_Text(debug_string);
    //             }
    //         } while ((status != 0) && (retries-- > 0));
    //         ReleaseMutex(ghMutex);
    //     }

    //     if(status != STATUS_OK)
    //     {
    //         SERIAL_COMMS_Get_Error_Text(debug_string);
    //     }
    // }

    return status;
}


int32_t VL53L0X_read_multi(uint8_t address, uint8_t index, uint8_t *pdata, int32_t count)
{
    int32_t status = STATUS_OK;

    // int32_t readDataCount = count;
    // unsigned int retries = 3;
    // DWORD dwWaitResult;

    uint8_t outbuf;
    struct i2c_rdwr_ioctl_data packets;
    struct i2c_msg messages[2];

#ifdef VL53L0X_LOG_ENABLE
    int32_t      i = 0;
    char   value_as_str[VL53L0X_MAX_STRING_LENGTH_PLT];
    char *pvalue_as_str;
#endif

    outbuf = index;
    messages[0].addr    = gDevInfo.address;
    messages[0].flags   = 0;
    messages[0].len     = sizeof(outbuf);
    messages[0].buf     = &outbuf;

    messages[1].addr    = gDevInfo.address;
    messages[1].flags   = I2C_M_RD;
    messages[1].len     = (unsigned short)count;
    messages[1].buf     = pdata;

    packets.msgs = messages;
    packets.nmsgs = 2;

    pthread_mutex_lock(&ghMutex);

    if (gDevInfo.fd > 0) {
        if (ioctl(gDevInfo.fd, I2C_RDWR, &packets) < 0) {
            status = STATUS_FAIL;
        }
    }
    else {
        status = STATUS_FAIL;
    }

    pthread_mutex_unlock(&ghMutex);

    // dwWaitResult = WaitForSingleObject(ghMutex, INFINITE);
    // if(dwWaitResult == WAIT_OBJECT_0)
    // {
    //     /* The serial comms interface requires multiples of 4 bytes so we
    //      * must apply padding if required.
    //      */
    //     if((count % 4) != 0)
    //     {
    //         readDataCount = (4*(count/4)) + 4;
    //     }

    //     if(readDataCount > MAX_MSG_SIZE)
    //     {
    //         status = STATUS_FAIL;
    //     }

    //     if(status == STATUS_OK)
    //     {
    //         do
    //         {
    //             status = SERIAL_COMMS_Read_UBOOT(address, 0, index, _dataBytes, readDataCount);
    //             if(status == STATUS_OK)
    //             {
    //                 memcpy(pdata, &_dataBytes, count);
    //             }
    //             else
    //             {
    //                 SERIAL_COMMS_Get_Error_Text(debug_string);
    //             }
                    
    //         } while ((status != 0) && (retries-- > 0));
    //     }
    //     ReleaseMutex(ghMutex);
    // }

    // if(status != STATUS_OK)
    // {
    //     SERIAL_COMMS_Get_Error_Text(debug_string);
    // }

#ifdef VL53L0X_LOG_ENABLE

    // Build  value as string;
    pvalue_as_str =  value_as_str;

    for(i = 0 ; i < count ; i++)
    {
        sprintf(pvalue_as_str, "%02X", *(pdata+i));
        pvalue_as_str += 2;
    }

    trace_i2c("Read  reg : 0x%04X, Val : 0x%s\n", index, value_as_str);
#endif

    return status;
}


int32_t VL53L0X_write_byte(uint8_t address, uint8_t index, uint8_t data)
{
    int32_t status = STATUS_OK;
    const int32_t cbyte_count = 1;

#ifdef VL53L0X_LOG_ENABLE
    trace_print(TRACE_LEVEL_INFO,"Write reg : 0x%02X, Val : 0x%02X\n", index, data);
#endif

    status = VL53L0X_write_multi(address, index, &data, cbyte_count);

    return status;
}


int32_t VL53L0X_write_word(uint8_t address, uint8_t index, uint16_t data)
{
    int32_t status = STATUS_OK;

    uint8_t  buffer[BYTES_PER_WORD];

    // Split 16-bit word into MS and LS uint8_t
    buffer[0] = (uint8_t)(data >> 8);
    buffer[1] = (uint8_t)(data &  0x00FF);

    if (index%2 == 1)
    {
        status = VL53L0X_write_multi(address, index, &buffer[0], 1);
        status = VL53L0X_write_multi(address, index + 1, &buffer[1], 1);
        // serial comms cannot handle word writes to non 2-byte aligned registers.
    }
    else
    {
        status = VL53L0X_write_multi(address, index, buffer, BYTES_PER_WORD);
    }

    return status;
}


int32_t VL53L0X_write_dword(uint8_t address, uint8_t index, uint32_t data)
{
    int32_t status = STATUS_OK;
    uint8_t  buffer[BYTES_PER_DWORD];

    // Split 32-bit word into MS ... LS bytes
    buffer[0] = (uint8_t) (data >> 24);
    buffer[1] = (uint8_t)((data &  0x00FF0000) >> 16);
    buffer[2] = (uint8_t)((data &  0x0000FF00) >> 8);
    buffer[3] = (uint8_t) (data &  0x000000FF);

    status = VL53L0X_write_multi(address, index, buffer, BYTES_PER_DWORD);

    return status;
}


/**
 * Read a BYTE from target device by i2c.
 * 
 * @param address I2C address of the device.
 * @param index Register want to read.
 * @param pdata A pointer to the buffer.
 * @return STATUS_OK if success. 
 */ 
int32_t VL53L0X_read_byte(uint8_t address, uint8_t index, uint8_t *pdata)
{
    int32_t status = STATUS_OK;
    int32_t cbyte_count = 1;

    status = VL53L0X_read_multi(address, index, pdata, cbyte_count);

#ifdef VL53L0X_LOG_ENABLE
    trace_print(TRACE_LEVEL_INFO,"Read reg : 0x%02X, Val : 0x%02X\n", index, *pdata);
#endif

    return status;
}


/**
 * Read a WORD from target device by i2c.
 * 
 * @param address I2C address of the device.
 * @param index Register want to read.
 * @param pdata A pointer to the buffer.
 * @return STATUS_OK if success.
 */ 
int32_t VL53L0X_read_word(uint8_t address, uint8_t index, uint16_t *pdata)
{
    int32_t status = STATUS_OK;
    uint8_t buffer[BYTES_PER_WORD];

    status = VL53L0X_read_multi(address, index, buffer, BYTES_PER_WORD);
    *pdata = ((uint16_t)buffer[0]<<8) + (uint16_t)buffer[1];

    return status;

}


/**
 * Read a DWORD from target device by i2c.
 * 
 * @param address I2C address of the device.
 * @param index Register want to read.
 * @param pdata A pointer to the buffer.
 * @return STATUS_OK if success.
 */
int32_t VL53L0X_read_dword(uint8_t address, uint8_t index, uint32_t *pdata)
{
    int32_t status = STATUS_OK;
    uint8_t buffer[BYTES_PER_DWORD];

    status = VL53L0X_read_multi(address, index, buffer, BYTES_PER_DWORD);
    *pdata = ((uint32_t)buffer[0]<<24) + ((uint32_t)buffer[1]<<16) + ((uint32_t)buffer[2]<<8) + (uint32_t)buffer[3];

    return status;
}
