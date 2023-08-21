int g_evil_variable = 666;

int wilma() {
  static int v = 1;
  v++;
  return v;
}

int *bar() {
  int *space = new int[100000];
  return space;
}

int *fred() {
  int *space = new int;
  return space;
}

int foo() {
  int x = 1;
  x ++;
  return x;
}

int main() {
  int y = 2;
  y += foo();

  int *p = bar();
  int i;
  for(i = 0; i < 100000; i++) {
    p[i] = i*i;
  }
  int sum = 0;
  for(i = 0; i < 100000; i++) {
    sum += p[i];
  }
  std::cout << "sum: " << sum << std::endl;
  delete [] p;
  p = 0;

  // delete [] p;

  p = fred();
  delete fred;
  p = 0;

  i = wilma();
  i = wilma();
  i = wilma();
  i = wilma();


  return y;
}
