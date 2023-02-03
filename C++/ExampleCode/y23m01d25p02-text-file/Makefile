CXX := g++
CXXFLAGS := -std=c++11
CXXFLAGS := $(CXXFLAGS) -Wall -Wpedantic -Wextra -Werror

all: main

main: main.o
	$(CXX) $(CXXFLAGS) -o main main.o

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp

# remove any derived files, to prepare for a clean build
clean:
	-rm -f main
	-rm -f *.o
	-rm -f *~
