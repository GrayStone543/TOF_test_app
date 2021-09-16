#if !defined(UTILS_H)
#define UTILS_H

#include "vl53l0x_def.h"


int VL53L0X_i2c_init(void);

int single_ranging(void);
int single_ranging_high_accuracy(void);
int single_ranging_long_range(void);
int continuous_ranging(void);

void print_pal_error(VL53L0X_Error Status);
void print_range_status(VL53L0X_RangingMeasurementData_t* pRangingMeasurementData);

#endif // UTILS_H