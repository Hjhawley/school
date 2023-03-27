#ifndef _BAG_H_
#define _BAG_H_
class Bag {
public:
  Bag();
  Bag(const int& i);
  int getItem() const;
  void setItem(const int& i);
  bool operator<(const Bag& rhs) const;
private:
  int mItem;
};

/*
std::ostream& operator<<(std::ostream& os, const Bag& b);
std::istream& operator>>(std::istream& is, const Bag& b);
*/

#endif /* _BAG_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
