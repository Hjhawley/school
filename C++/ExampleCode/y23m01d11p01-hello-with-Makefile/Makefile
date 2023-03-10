all: hello

hello: hello.o
	g++ -std=c++11 -o hello hello.o

hello.o: hello.cpp
	g++ -std=c++11 -c hello.cpp