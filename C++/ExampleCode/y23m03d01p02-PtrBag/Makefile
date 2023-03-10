CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
# CXXFLAGS := $(CXXFLAGS) -g
TARGETS := main

all: $(TARGETS)

main: main.o PtrBag.o Data.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp PtrBag.h Data.h
	$(CXX) $(CXXFLAGS) -c $<

PtrBag.o: PtrBag.cpp PtrBag.h Data.h
	$(CXX) $(CXXFLAGS) -c $<

Data.o: Data.cpp Data.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o *~ $(TARGETS)
