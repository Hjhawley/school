CXX := g++
CXXFLAGS := -std=c++11
# extra tough syntax error and bad code style warning checking
CXXFLAGS := $(CXXFLAGS) -Wall -Wpedantic -Wextra -Werror
# add debugging information to the program
CXXFLAGS := -g

all: vector_example

vector_example: vector_example.o picture_creation.o picture_output.o
	$(CXX) $(CXXFLAGS) -o vector_example vector_example.o picture_creation.o picture_output.o

vector_example.o: vector_example.cpp ascii_functions.h
	$(CXX) $(CXXFLAGS) -c vector_example.cpp

picture_creation.o: picture_creation.cpp ascii_functions.h
	$(CXX) $(CXXFLAGS) -c picture_creation.cpp

picture_output.o: picture_output.cpp ascii_functions.h
	$(CXX) $(CXXFLAGS) -c picture_output.cpp


# remove any derived files, to prepare for a clean build
clean:
	-rm -f vector_example
	-rm -f *.o
	-rm -f *~
