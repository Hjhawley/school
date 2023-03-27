#ifndef _BAG_H_
#define _BAG_H_
class Bag {
public:
  Bag();
  Bag(const int& i);
  int getItem() const;
  void setItem(const int& i);
private:
  int mItem;
};

#endif /* _BAG_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
