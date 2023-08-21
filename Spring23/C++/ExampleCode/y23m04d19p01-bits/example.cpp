int foo(unsigned int flags) {
  if(flags & DO_RECURSION) {
  }
  ...
}

int main() {
  int x = foo(DO_LOOP | DO_GREEN | DO_BAR);
}
