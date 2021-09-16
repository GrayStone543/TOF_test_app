#include <stdio.h>
#include <stdlib.h>

#include "utils.h"



int main(int argc, char ** argv)
{
    int mode = 0;

    if (argc == 1) {

    }
    else if (argc == 2) {
        mode = atoi(argv[1]);
    }
    else {
        printf("USAGE : %s [Test mode] \n", argv[0]);
        printf("\tTest mode:\n");
        printf("\t\t0 = Single Ranging\n");
        printf("\t\t1 = Continuous Ranging\n");
        printf("\t\t2 = Single Ranging High Accuracy\n");
        printf("\t\t3 = Single Ranging Long Range\n");
        return 1;
    }

    switch (mode)
    {
    case 1:
        continuous_ranging();
        break;
    case 2:
        single_ranging_high_accuracy();
        break;
    case 3:
        single_ranging_long_range();
        break;
    default:
        single_ranging();
    }
    
    return 0;
}