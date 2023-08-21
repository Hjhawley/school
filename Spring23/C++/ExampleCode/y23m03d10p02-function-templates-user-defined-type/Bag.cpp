#include "Bag.h"

Bag::Bag()
  : mItem(0) {
}

Bag::Bag(const int& i) 
  : mItem(i) {
}
int Bag::getItem() const {
  return mItem;
}
void Bag::setItem(const int& i) {
  mItem = i;
}
