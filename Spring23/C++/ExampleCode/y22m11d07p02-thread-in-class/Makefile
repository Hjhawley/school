CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
#CXXFLAGS := $(CXXFLAGS) -g
LDFLAGS := -lpthread

all: primes

primes: main.o prime.o PrimeHunter.o
	$(CXX) $(CXXFLAGS) -o $@ $^ $(LDFLAGS)

main.o: main.cpp prime_utils.h
	$(CXX) $(CXXFLAGS) -c $<

prime.o: prime.cpp prime_utils.h
	$(CXX) $(CXXFLAGS) -c $<

PrimeHunter.o: PrimeHunter.cpp PrimeHunter.h prime_utils.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *~
	-rm -f *.o
	-rm -f primes
