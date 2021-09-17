CC ?= gcc
RM ?= rm
AR ?= ar

CFLAGS ?= -Wall

TARGET = libvl53l0x.a

#SUB_DIR = core platform

INCDIR = core/inc platform/inc
OBJDIR = obj
COREDIR = core/src
PLATFORMDIR = platform/src

CORE_FILES = vl53l0x_api_calibration.c vl53l0x_api_core.c vl53l0x_api_ranging.c vl53l0x_api_strings.c vl53l0x_api.c
PLATFORM_FILES = vl53l0x_platform_log.c vl53l0x_platform.c vl53l0x_i2c_linux.c

INC = $(foreach d, $(INCDIR), -I$d)
SOURCES = $(CORE_FILES) $(PLATFORM_FILES)
OBJECTS = $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))

all: $(TARGET)

$(OBJDIR)/%.o: $(COREDIR)/%.c
	$(CC) $(CFLAGS) $(INC) -c -o $@ $<

$(OBJDIR)/%.o: $(PLATFORMDIR)/%.c
	$(CC) $(CFLAGS) $(INC) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)

$(TARGET): $(OBJDIR) $(OBJECTS)
	$(AR) rcs $(TARGET) $(OBJECTS)

#build_sub:
#	@for s in $(SUB_DIR); do \
#	$(MAKE) -C $$s;\
#	done

#$(TARGET): build_sub
#	$(AR) rcs $(TARGET)

clean:
	@$(RM) -rf $(OBJDIR)
	@$(RM) -f $(TARGET)

.PHONY: clean all
