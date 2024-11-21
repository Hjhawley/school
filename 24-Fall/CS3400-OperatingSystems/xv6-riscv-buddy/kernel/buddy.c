#include "types.h"
#include "defs.h"
#include "spinlock.h"
#include "param.h"
#include "memlayout.h"
#include "riscv.h"
#include "proc.h"

struct spinlock buddy_lock;

void buddyinit(void) {
    initlock(&buddy_lock, "buddy_lock");
}

struct buddy_header {
    uint64 magic;       // Magic number to identify allocated/free blocks
    uint64 size;        // Size of the block (including header)
    struct buddy_header *next;  // Pointer to next free block (only for free blocks)
};

#define MIN_ORDER 5    // 2^5 = 32 bytes
#define MAX_ORDER 12   // 2^12 = 4096 bytes
#define NUM_ORDERS (MAX_ORDER - MIN_ORDER + 1)

struct buddy_header *free_lists[NUM_ORDERS];

void buddy_print_helper(void *block, int size, int depth) {
    // Base case: if the block is not split, print its status and size
    // Recursive case: if the block is split, call the function on both halves
}

void buddy_print(void *ptr) {
    // Find the starting address of the 4096-byte block containing ptr
    // Call buddy_print_helper with the starting address and size 4096
}

#define MAGIC_ALLOCATED 0xBADDCAFEDEADBEEF
#define MAGIC_FREE      0xDEADBEEFCAFEBADD

int size_to_order(uint64 size);
uint64 order_to_size(int order);
struct buddy_header* find_buddy(struct buddy_header* block);

#define alignup(x, align) (((x) + (align) - 1) & ~((align) - 1))

void* buddy_alloc(uint64 length) {
    if (length == 0 || length > 4080) {
        return 0;
    }

    // Include header size
    uint64 total_size = length + sizeof(struct buddy_header);

    // Find the appropriate order
    int order = MIN_ORDER;
    uint64 block_size = 1 << order;
    while (block_size < total_size && order <= MAX_ORDER) {
        order++;
        block_size <<= 1;
    }

    if (order > MAX_ORDER) {
        return 0; // Requested size too big
    }

    acquire(&buddy_lock);

    // Find a free block or split a larger one
    // ...

    release(&buddy_lock);

    // Return pointer to usable memory (after the header)
    return (void *)((char *)block + sizeof(struct buddy_header));
}
