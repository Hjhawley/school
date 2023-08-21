TARGETS := 01_exception 02_exception \
	03_exception 04_exception \
	05_exception 06_exception \
	07_exception 08_exception \
	09_exception \
	08a_exception 10_exception

extra_junk := 

CXXFLAGS := -Wall

all: $(TARGETS)

check: $(TARGETS)
	./01_exception; echo ""; echo ""
	./02_exception; echo ""; echo ""
	./03_exception; echo ""; echo ""
	./04_exception; echo ""; echo ""
	./05_exception; echo ""; echo ""
	./06_exception; echo ""; echo ""
	./07_exception; echo ""; echo ""
	./08_exception; echo ""; echo ""
	./08a_exception; echo ""; echo ""
	./09_exception; echo ""; echo ""
	./10_exception; echo ""; echo ""

%_exception: %_exception.cpp
	$(CXX) $(CXXFLAGS) -o $@ $^


clean:
	-rm -f *~
	-rm -f $(TARGETS) $(extra_junk)
	-rm -f *.o

