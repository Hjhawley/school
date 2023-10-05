CXX := g++
CXXFLAGS := -Wall -Wextra -Wpedantic -Werror

main: main.o Bag.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp Bag.h functions.h
	$(CXX) $(CXXFLAGS) -c $<

Bag.o: Bag.cpp Bag.h
	$(CXX) $(CXXFLAGS) -c $<



