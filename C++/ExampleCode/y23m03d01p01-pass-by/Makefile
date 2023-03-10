CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
# CXXFLAGS := $(CXXFLAGS) -g
TARGETS := main main2

all: $(TARGETS)

main2: main2.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main2.o: main2.cpp
	$(CXX) $(CXXFLAGS) -c $<

main: main.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o *~ $(TARGETS)
