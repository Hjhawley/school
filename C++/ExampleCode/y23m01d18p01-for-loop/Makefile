CXXFLAGS := -std=c++11
CXXFLAGS := $(CXXFLAGS) -Wall -Wpedantic -Wextra -Werror
### debugging flag
CXXFLAGS := $(CXXFLAGS) -g

all: adder guessing

guessing: guessing.o controllers.o user_io.o
	$(CXX) $(CXXFLAGS) -o guessing guessing.o controllers.o user_io.o

guessing.o: guessing.cpp functions.h
	$(CXX) $(CXXFLAGS) -c guessing.cpp

adder: adder.o user_io.o controllers.o
	$(CXX) $(CXXFLAGS) -o adder adder.o user_io.o controllers.o

adder.o: adder.cpp functions.h
	$(CXX) $(CXXFLAGS) -c adder.cpp

controllers.o: controllers.cpp functions.h
	$(CXX) $(CXXFLAGS) -c controllers.cpp

user_io.o: user_io.cpp functions.h
	$(CXX) $(CXXFLAGS) -c user_io.cpp

clean:
	-rm -f *.o adder guessing *~
