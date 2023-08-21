CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
# CXXFLAGS := $(CXXFLAGS) -g
TARGETS := main

all: $(TARGETS)

main: main.o modify.o display.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp functions.h
	$(CXX) $(CXXFLAGS) -c $<

modify.o: modify.cpp functions.h
	$(CXX) $(CXXFLAGS) -c $<

display.o: display.cpp functions.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o *~ $(TARGETS)


