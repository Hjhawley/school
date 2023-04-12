#include <iostream>

/*
 * Uses exceptions from new to find
 * largest amount of memory that can
 * be allocated.
 */

char *allocate_space( long size ) {
  char *myarray = new char[ size ];
  return myarray;
}


int main( ) {
  char *x = 0;
  long largest_ok = 0;
  long smallest_not_ok = 0;
  long size = 1;
  while( smallest_not_ok == 0 ) {
    try {
      std::cout << "Trying to allocate " << size << " bytes...";
      x = allocate_space( size );
      std::cout << "OK" << std::endl;
      largest_ok = size;
      delete [] x;
      x = 0;
    } catch ( std::exception &e ) {
      std::cout << "FAIL" << std::endl;
      smallest_not_ok = size;
    }
    size *= 2;
  }
  std::cout << "largest_ok = " << largest_ok << std::endl;
  std::cout << "smallest_not_ok = " << smallest_not_ok << std::endl;
  while( smallest_not_ok > largest_ok + 1 ) {
    size = ( largest_ok + smallest_not_ok ) / 2;
    try {
      std::cout << "Trying to allocate " << size << " bytes...";
      x = allocate_space( size );
      std::cout << "OK" << std::endl;
      largest_ok = size;
      delete [] x;
      x = 0;
    } catch ( std::exception &e ) {
      std::cout << "FAIL" << std::endl;
      smallest_not_ok = size;
    }
  }
  std::cout << "largest_ok = " << largest_ok << std::endl;
  std::cout << "smallest_not_ok = " << smallest_not_ok << std::endl;
  return 0;
}
