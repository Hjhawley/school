#ifndef _PTRBAG_H_
#define _PTRBAG_H_
#include "Data.h"

class PtrBag {
public:
  PtrBag();
  ~PtrBag();
  void setData(Data *p);
  Data& getData();
  const Data& getData() const;
private:
  Data *mPtr;
};

#endif /* _PTRBAG_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
