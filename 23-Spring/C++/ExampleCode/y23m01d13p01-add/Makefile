all: adder guessing

guessing: guessing.o
	g++ -std=c++11 -o guessing guessing.o

guessing.o: guessing.cpp
	g++ -std=c++11 -c guessing.cpp

adder: adder.o user_io.o controllers.o
	g++ -std=c++11 -o adder adder.o user_io.o controllers.o

adder.o: adder.cpp functions.h
	g++ -std=c++11 -c adder.cpp

controllers.o: controllers.cpp functions.h
	g++ -std=c++11 -c controllers.cpp

user_io.o: user_io.cpp functions.h
	g++ -std=c++11 -c user_io.cpp

