#ifndef _FUNCTIONS_H_
#define _FUNCTIONS_H_

template <class T>
T minimum(T x, T y) {
  T z;
  if(x < y) {
    z = x;
  } else {
    z = y;
  }
  return z;
}

#endif /* _FUNCTIONS_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
