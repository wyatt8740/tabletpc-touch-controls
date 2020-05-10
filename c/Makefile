CC=gcc
CFLAGS=-g -Wall `pkg-config --cflags gtk+-3.0`
LDFLAGS=-lxcb `pkg-config --libs gtk+-3.0`

.PHONY: all

all: applet

applet: applet.c
	$(CC) -Wall -o applet applet.c $(CFLAGS) $(LDFLAGS)

.PHONY: clean

clean:
	rm -f applet *.o
