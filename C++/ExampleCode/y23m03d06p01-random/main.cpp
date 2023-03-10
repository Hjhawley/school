#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>

int main() {
  std::srand(std::time(0)); // seed once at the beginning of the program
  int mcv = 100;
  std::vector<int> counts(mcv+1, 0);

  unsigned int i;
  int r;
  for(i = 0; i < 1000000; i++) {
    r = std::rand() % (mcv+1); // generate random numbers as often as you want.
    // [0, mcv]
    // r = 1 + std::rand() % (mcv); // bumps both ends of range [1,mcv]
    counts[r]++;
    //std::cout << i << " " << r << std::endl;
  }

  for(i = 0; i < counts.size(); i++) {
    std::cout << i << " " << counts[i] << std::endl;
  }
  return 0;
}
