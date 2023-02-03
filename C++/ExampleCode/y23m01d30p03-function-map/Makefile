CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
# CXXFLAGS := $(CXXFLAGS) -g
TARGETS := calculator

all: $(TARGETS)

calculator: calculator.o calculator_controllers.o calculator_operations.o
	$(CXX) $(CXXFLAGS) -o $@ $^

calculator.o: calculator.cpp calculator.h
	$(CXX) $(CXXFLAGS) -c $<

calculator_controllers.o: calculator_controllers.cpp calculator.h
	$(CXX) $(CXXFLAGS) -c $<

calculator_operations.o: calculator_operations.cpp calculator.h
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f *.o *~ $(TARGETS)
