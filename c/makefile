CC = gcc
RM = rm

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


$(OBJDIR)/%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(OBJDIR):
	@mkdir -p $(OBJDIR)


.PHONY: clean
clean:
	make -C vl53l0x_api clean
	$(RM) -f $(OBJDIR)/*.o ranging
