CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
LDFLAGS := -lpthread

all: main main-2thread main-2thread-1count main-2thread-balanced

main: main.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c $<


main-2thread: main-2thread.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main-2thread.o: main-2thread.cpp
	$(CXX) $(CXXFLAGS) -c $<

main-2thread-1count: main-2thread-1count.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main-2thread-1count.o: main-2thread-1count.cpp
	$(CXX) $(CXXFLAGS) -c $<

main-2thread-balanced: main-2thread-balanced.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main-2thread-balanced.o: main-2thread-balanced.cpp
	$(CXX) $(CXXFLAGS) -c $<

