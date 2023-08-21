#include <iostream>
#include <string>
#include "Bag.h"
#include "BagOfValue.h"
#include "functions.h"

int main() {
  int a = 17;
  int b = 13;

  int c = minimum(a, b);
  std::cout << c << " is the minimum of " << a << " and " << b << std::endl;

  /////////////////////////////////////


  double f = 13.1;
  double g = 13.01;

  double h = minimum(f, g);
  std::cout << h << " is the minimum of " << f << " and " << g << std::endl;

  /////////////////////////////////////
  std::string s = "hello";
  std::string t = "help";

  std::string u = minimum(s, t);
  std::cout << u << " is the minimum of " << s << " and " << t << std::endl;

  /////////////////////////////////////
  Bag p(25);
  Bag q(24);

  Bag r = minimum(p, q);
  std::cout << r.getItem() << " is the minimum of " << p.getItem() << " and " << q.getItem() << std::endl;

  /////////////////////////////////////
  BagOfValue<std::string> b1;
  BagOfValue<std::string> b2;
  
  b1.push_back("hello");
  b1.push_back("world");
  
  b2.push_back("goodbye");
  b2.push_back("and");
  b2.push_back("thanks");
  b2.push_back("for");
  b2.push_back("all");
  b2.push_back("the");
  b2.push_back("fish");

  BagOfValue w = minimum(b1, b2);
  std::cout << w[0] << " is the minimum of " << b1[0] << " and " << b2[0] << std::endl;


  //
  //minimum(a, t);
  
  return 0;
}
