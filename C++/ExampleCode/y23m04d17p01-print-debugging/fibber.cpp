#include "fibber.h"
#include "debugger.h"

bigint fib(bigint n) {
  bigint f;
  if(n == 0) {
    f = 0;
  } else if(n == 1) {
    f = 1;
  } else if(n > 1) {
    f = fib(n-1) + fib(n-2);
  } else {
    f = -1;
  }
  return f;
}

bigint fib_memo(bigint n, std::vector<bigint>& memo) {
  DEBUG_MESSAGE("fib_memo(" << n << "): START");
  bigint f;
  if(memo[n] >= 0) {
    f = memo[n];
  } else if(n == 0) {
    f = 0;
  } else if(n == 1) {
    f = 1;
  } else if(n > 1) {
    f = fib_memo(n-1, memo) + fib_memo(n-2, memo);
  } else {
    f = -1;
  }
  memo[n] = f;
  DEBUG_MESSAGE("fib_memo(" << n << ") = "<< memo[n] <<": END");
  return f;
}
