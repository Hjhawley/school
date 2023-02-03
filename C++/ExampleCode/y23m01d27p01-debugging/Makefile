CXXFLAGS := -std=c++11
CXXFLAGS := $(CXXFLAGS) -Wall -Wpedantic -Wextra -Werror

main: main.o
	$(CXX) $(CXXFLAGS) -o main main.o

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c main.cpp
