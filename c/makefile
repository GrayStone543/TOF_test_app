CC = gcc
RM = rm

LIB_NAME := pyvl53l0x.so
API_SOURCES := vl53l0x_api_calibration.c vl53l0x_api_core.c vl53l0x_api_ranging.c vl53l0x_api_strings.c vl53l0x_api.c
API_SOURCES += vl53l0x_platform_log.c vl53l0x_platform.c vl53l0x_i2c_linux.c
API_OBJECTS := $(addprefix vl53l0x_api/obj/, $(SOURCES:.c=.o))

CFLAGS = -Wall

INCDIR = vl53l0x_api/core/inc vl53l0x_api/platform/inc
#SRCDIR = src
OBJDIR = obj

CFLAGS += $(foreach d, $(INCDIR), -I$d)

LDFLAGS = -Lvl53l0x_api -lvl53l0x

SOURCES := utils.c singleRanging.c continuousRanging.c singleRanging_High_Accuracy.c singleRanging_Long_Range.c main.c
OBJECTS := $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))


all: api $(OBJDIR) $(OBJECTS)
	$(CC) $(CFLAGS) -o ranging $(OBJECTS) $(LDFLAGS)

api:
	make -C vl53l0x_api

solib: api
	$(CC) $(CFLAGS) -fPIC -shared -o $(LIB_NAME) pyvl53l0x.c $(API_OBJECTS)


$(OBJDIR)/%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)


.PHONY: clean
clean:
	make -C vl53l0x_api clean
	$(RM) -f $(OBJDIR)/*.o ranging
