CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
LDFLAGS := -lpthread

all: main main-2thread main-2thread-1count main-2thread-balanced main-class

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

main-class: main-class.o PrimeHunter.o prime_utils.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main-class.o: main-class.cpp PrimeHunter.h
	$(CXX) $(CXXFLAGS) -c $<

PrimeHunter.o: PrimeHunter.cpp PrimeHunter.h prime_utils.h
	$(CXX) $(CXXFLAGS) -c $<

prime_utils.o: prime_utils.cpp prime_utils.h
	$(CXX) $(CXXFLAGS) -c $<

