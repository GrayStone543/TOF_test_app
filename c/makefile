export CC = gcc
export RM = rm

CFLAGS = -Wall

TARGET = ranging
SO_FILE := pyvl53l0x.so

APIDIR = vl53l0x_api
INCDIR = vl53l0x_api/core/inc vl53l0x_api/platform/inc
OBJDIR = obj


INC = $(foreach d, $(INCDIR), -I$d)


SO_OBJDIR = so_obj
CORE_SRC_DIR = $(APIDIR)/core/src
PLATFORM_SRC_DIR = $(APIDIR)/platform/src
CORE_FILES = vl53l0x_api_calibration.c vl53l0x_api_core.c vl53l0x_api_ranging.c vl53l0x_api_strings.c vl53l0x_api.c
PLATFORM_FILES = vl53l0x_platform_log.c vl53l0x_platform.c vl53l0x_i2c_linux.c
SO_SOURCES := pyvl53l0x.c $(CORE_FILES) $(PLATFORM_FILES)
SO_OBJECTS := $(addprefix $(SO_OBJDIR)/, $(SO_SOURCES:.c=.o))
SO_CFLAGS = -Wall -fPIC

LDFLAGS = -Lvl53l0x_api -lvl53l0x

SOURCES := utils.c singleRanging.c continuousRanging.c singleRanging_High_Accuracy.c singleRanging_Long_Range.c main.c
OBJECTS := $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))


all: $(TARGET)

api:
	$(MAKE) -C $(APIDIR)

$(TARGET): $(OBJDIR) $(OBJECTS)
	$(MAKE) -C $(APIDIR)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJECTS) $(LDFLAGS)

solib: $(SO_OBJDIR) $(SO_OBJECTS)
	$(CC) $(SO_CFLAGS) -shared -o $(SO_FILE) $(SO_OBJECTS)

#solib:
#	$(MAKE) -C $(API_DIR) CFLAGS='$(SO_CFLAGS)'
#	$(CC) $(CFLAGS) $(SO_CFLAGS) $(INC) -shared -o $(SO_FILE) pyvl53l0x.c $(LDFLAGS)

$(SO_OBJDIR)/%.o: $(CORE_SRC_DIR)/%.c
	$(CC) $(SO_CFLAGS) $(INC) -c -o $@ $<

$(SO_OBJDIR)/%.o: $(PLATFORM_SRC_DIR)/%.c
	$(CC) $(SO_CFLAGS) $(INC) -c -o $@ $<

$(SO_OBJDIR)/%.o: %.c
	$(CC) $(SO_CFLAGS) $(INC) -c -o $@ $<

$(SO_OBJDIR):
	@mkdir -p $(SO_OBJDIR)

$(OBJDIR)/%.o: %.c
	$(CC) $(CFLAGS) $(INC) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)

clean:
	$(MAKE) -C $(APIDIR) clean
	@$(RM) -f $(TARGET) $(SO_FILE)
	@$(RM) -rf $(OBJDIR)
	@$(RM) -rf $(SO_OBJDIR)

.PHONY: clean all
