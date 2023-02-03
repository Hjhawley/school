all: class_example

class_example: class_example.o Point.o Point3D.o
	g++ -std=c++11 -Wall -Werror -Wpedantic -Wextra -o class_example class_example.o Point.o Point3D.o

class_example.o: class_example.cpp Point.h Point3D.h
	g++ -std=c++11 -Wall -Werror -Wpedantic -Wextra -c class_example.cpp

Point.o: Point.cpp Point.h
	g++ -std=c++11 -Wall -Werror -Wpedantic -Wextra -c Point.cpp

Point3D.o: Point3D.cpp Point3D.h Point.h
	g++ -std=c++11 -Wall -Werror -Wpedantic -Wextra -c Point3D.cpp

clean:
	-rm -f *.o
	-rm -f class_example
	-rm -f *~
