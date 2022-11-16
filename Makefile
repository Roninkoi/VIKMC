CC = gcc
CCFLAGS = -std=gnu11 -lm -O3

.PHONY: clean all
.DEFAULT: all

all: vikmc

clean:
	rm -f vikmc
	rm -f *.o

vikmc: kmc.c kmc.h
	$(CC) $(CCFLAGS) -o vikmc kmc.c kmc.h mt19937-64.c
