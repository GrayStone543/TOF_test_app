OBJDIR = obj
SRCDIR = src
INCDIR = inc ../core/inc

INC = $(foreach d, $(INCDIR), -I$d)

SOURCES = \
  vl53l0x_i2c_linux.c \
  vl53l0x_platform_log.c \
  vl53l0x_platform.c

OBJECTS := $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))

all: $(OBJDIR) $(OBJECTS)

$(OBJDIR)/%.o: $(SRCDIR)/%.c
	$(CC) $(CFLAGS) $(INC) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)

clean:
	$(RM) -rf $(OBJDIR)

.PHONY: clean all
