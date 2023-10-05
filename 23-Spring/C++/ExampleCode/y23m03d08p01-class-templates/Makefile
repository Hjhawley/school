CXX := g++
CXXFLAGS := -Wall -Wextra -Wpedantic -Werror -g
OBJECTS := main.o BagOfInt.o BagOfDouble.o

main: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp BagOfInt.h BagOfDouble.h
	$(CXX) $(CXXFLAGS) -c $<

BagOfInt.o: BagOfInt.cpp BagOfInt.h
	$(CXX) $(CXXFLAGS) -c $<

BagOfDouble.o: BagOfDouble.cpp BagOfDouble.h
	$(CXX) $(CXXFLAGS) -c $<


clean:
	-rm -f *.o main
