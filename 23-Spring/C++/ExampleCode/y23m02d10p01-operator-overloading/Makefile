CXX := g++
CXXFLAGS := -std=c++11
# extra tough syntax error and bad code style warning checking
CXXFLAGS := $(CXXFLAGS) -Wall -Wpedantic -Wextra -Werror
#
#CXXFLAGS := $(CXXFLAGS) -g
TARGETS := fraction_calculator


all: $(TARGETS)

fraction_calculator: fraction_calculator.o controllers.o user_io.o Fraction.o actions.o
	$(CXX) $(CXXFLAGS) -o fraction_calculator fraction_calculator.o controllers.o user_io.o Fraction.o actions.o

fraction_calculator.o: fraction_calculator.cpp functions.h Fraction.h
	$(CXX) $(CXXFLAGS) -c fraction_calculator.cpp

controllers.o: controllers.cpp functions.h Fraction.h
	$(CXX) $(CXXFLAGS) -c controllers.cpp

user_io.o: user_io.cpp functions.h Fraction.h
	$(CXX) $(CXXFLAGS) -c user_io.cpp

actions.o: actions.cpp functions.h Fraction.h
	$(CXX) $(CXXFLAGS) -c actions.cpp

Fraction.o: Fraction.cpp Fraction.h
	$(CXX) $(CXXFLAGS) -c Fraction.cpp

# remove any derived files, to prepare for a clean build
clean:
	-rm -f $(TARGETS)
	-rm -f *.o
	-rm -f *~
