OBJDIR = obj
SRCDIR = src
INCDIR = inc ../platform/inc

INC = $(foreach d, $(INCDIR), -I$d)

SOURCES = \
  vl53l0x_api_calibration.c \
  vl53l0x_api_core.c \
  vl53l0x_api_ranging.c \
  vl53l0x_api_strings.c \
  vl53l0x_api.c

OBJECTS := $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))

all: $(OBJDIR) $(OBJECTS)

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) $(INC) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)

clean:
	$(RM) -rf $(OBJDIR)

.PHONY: clean all
