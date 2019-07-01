
.PHONY = all clean

CC = python3

FILE = main.py

SRCS := $(wildcard ./Tests/*.cl)
BINS := $(SRCS:%.cl=%)

all: ${BINS}

%: %.cl
	${CC} ${FILE} $<

clean:
	rm -rf ./Tests/*.mips