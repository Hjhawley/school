CXXFLAGS := -std=c++11

main: main.o X.o Y.o
	g++ $(CXXFLAGS) -o $@ $^

main.o: main.cpp X.h Y.h
	g++ $(CXXFLAGS) -c $<

X.o: X.cpp X.h
	g++ $(CXXFLAGS) -c $<

Y.o: Y.cpp X.h Y.h
	g++ $(CXXFLAGS) -c $<

