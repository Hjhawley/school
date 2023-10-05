CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
LDFLAGS := -lpthread

all: main main-2thread

main: main.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c $<


main-2thread: main-2thread.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main-2thread.o: main-2thread.cpp
	$(CXX) $(CXXFLAGS) -c $<
