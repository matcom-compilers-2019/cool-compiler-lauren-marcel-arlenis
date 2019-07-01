.PHONY = main clean

CC = ./coolc.sh

SRCS := $(wildcard ./Tests/*.cl)
BINS := $(SRCS:%.cl=%)

main: ${BINS}

%: %.cl
	${CC} ${FILE} $<

clean:
	rm -rf ./Tests/*.mips