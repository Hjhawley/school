// spinlock.h
#ifndef SPINLOCK_H
#define SPINLOCK_H

struct spinlock {
  uint locked;       // Is the lock held?

  // For debugging:
  char *name;        // Name of lock.
  struct cpu *cpu;   // The CPU holding the lock.
};

void initlock(struct spinlock*, char*);
void acquire(struct spinlock*);
void release(struct spinlock*);
int  holding(struct spinlock*);

#endif // SPINLOCK_H
