CXX := g++
CXXFLAGS := -Wall -Wextra -Wpedantic -Werror

main: main.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp functions.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o main *~

