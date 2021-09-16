CC = gcc
RM = rm

CFLAGS = -Wall

INCDIR = vl53l0x_api/core/inc vl53l0x_api/platform/inc
#SRCDIR = src
OBJDIR = obj

CFLAGS += $(foreach d, $(INCDIR), -I$d)

LDFLAGS = -Lvl53l0x_api -lvl53l0x

SOURCES := singleRanging.c
OBJECTS := $(addprefix $(OBJDIR)/, $(SOURCES:.c=.o))


all: $(OBJDIR) $(OBJECTS)
	$(CC) $(CFLAGS) -o single_ranging $(OBJECTS) $(LDFLAGS)

$(OBJDIR)/singleRanging.o: singleRanging.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)

.PHONY: clean
clean:
	$(RM) -f $(OBJDIR)/*.o single_ranging
