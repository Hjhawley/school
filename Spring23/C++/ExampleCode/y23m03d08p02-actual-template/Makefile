CXX := g++
CXXFLAGS := -Wall -Wextra -Wpedantic -Werror -g
OBJECTS := main.o

main: $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp BagOfValue.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o main
