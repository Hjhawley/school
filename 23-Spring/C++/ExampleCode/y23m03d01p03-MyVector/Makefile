CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
# CXXFLAGS := $(CXXFLAGS) -g
TARGETS := main

all: $(TARGETS)

main: main.o MyVector.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp MyVector.h
	$(CXX) $(CXXFLAGS) -c $<

MyVector.o: MyVector.cpp MyVector.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o *~ $(TARGETS)
