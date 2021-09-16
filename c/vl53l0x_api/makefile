CC = gcc
RM = rm
AR = ar

CFLAGS = -Wall -Icore/inc -Iplatform/inc

SRCDIR = src
OBJDIR = obj

SOURCES := vl53l0x_api_calibration.c vl53l0x_api_core.c vl53l0x_api_ranging.c vl53l0x_api_strings.c vl53l0x_api.c
SOURCES += vl53l0x_platform_log.c vl53l0x_platform.c vl53l0x_i2c_linux.c
OBJECTS := $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))

all: $(OBJDIR) $(OBJECTS)
	$(AR) rcs libvl53l0x.a $(OBJECTS)

$(OBJDIR)/%.o: core/$(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR)/%.o: platform/$(SRCDIR)/%.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)

.PHONY: clean
clean:
	$(RM) -f $(OBJDIR)/*.o libvl53l0x.a
