CXX := g++
CXXFLAGS := -std=c++11 -Wall
LDFLAGS := -lpthread

all: main-balanced

main-balanced: main-balanced.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main-balanced.o: main-balanced.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o *~ main-balanced
