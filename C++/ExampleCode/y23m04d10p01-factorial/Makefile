CXX := g++
CXXFLAGS := -std=c++11 -Wall -Wextra -Wpedantic -Werror
LDFLAGS := -lpthread
TARGETS := main main_no_loop fib_no_loop fib_with_loop fib_with_memo

all: $(TARGETS)

main: main.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main.o: main.cpp
	$(CXX) $(CXXFLAGS) -c $<

main_no_loop: main_no_loop.o
	$(CXX) $(CXXFLAGS) -o $@ $^

main_no_loop.o: main_no_loop.cpp
	$(CXX) $(CXXFLAGS) -c $<

fib_no_loop: fib_no_loop.o
	$(CXX) $(CXXFLAGS) -o $@ $^

fib_no_loop.o: fib_no_loop.cpp
	$(CXX) $(CXXFLAGS) -c $<

fib_with_loop: fib_with_loop.o
	$(CXX) $(CXXFLAGS) -o $@ $^

fib_with_loop.o: fib_with_loop.cpp
	$(CXX) $(CXXFLAGS) -c $<

fib_with_memo: fib_with_memo.o
	$(CXX) $(CXXFLAGS) -o $@ $^

fib_with_memo.o: fib_with_memo.cpp
	$(CXX) $(CXXFLAGS) -c $<

clean:
	-rm -f $(TARGETS) *~ *.o
