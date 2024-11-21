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
    // Initialize free_lists to NULL
    for (int i = 0; i < NUM_ORDERS; i++) {
        free_lists[i] = NULL;
    }
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

#define MAGIC_ALLOCATED 0xBADDCAFEDEADBEEF
#define MAGIC_FREE      0xDEADBEEFCAFEBADD

int size_to_order(uint64 size) {
    int order = 0;
    uint64 sz = size;
    while (sz >>= 1) {
        order++;
    }
    return order;
}

uint64 order_to_size(int order) {
    return 1UL << order;
}

struct buddy_header* find_buddy(struct buddy_header* block) {
    uint64 addr = (uint64)block;
    uint64 size = block->size;
    uint64 buddy_addr = addr ^ size;
    return (struct buddy_header*)buddy_addr;
}

void buddy_print_helper(uint64 base_addr, int order, int depth) {
    for (int i = 0; i < depth; i++) {
        printf("       ");
    }

    uint64 size = 1UL << order;
    struct buddy_header* block = (struct buddy_header*)base_addr;

    // Check if the block is allocated
    if (block->magic == MAGIC_ALLOCATED) {
        printf("└──── used (%lu)\n", size);
        return;
    }

    // Check if the block is free
    int is_free = 0;
    struct buddy_header* curr = free_lists[order - MIN_ORDER];
    while (curr) {
        if ((uint64)curr == base_addr) {
            is_free = 1;
            break;
        }
        curr = curr->next;
    }

    if (is_free) {
        printf("└──── free (%lu)\n", size);
        return;
    }

    // If neither allocated nor free, it must be split
    printf("└──── split (%lu)\n", size);

    // Recursively print the two halves
    if (order > MIN_ORDER) {
        buddy_print_helper(base_addr, order - 1, depth + 1);
        buddy_print_helper(base_addr + (1UL << (order - 1)), order - 1, depth + 1);
    }
}

void buddy_print(void *ptr) {
    // Find the starting address of the 4096-byte block containing ptr
    uint64 addr = (uint64)ptr;
    uint64 base_addr = addr & ~((1UL << MAX_ORDER) - 1);

    printf("\n");
    buddy_print_helper(base_addr, MAX_ORDER, 0);
}

void buddy_test(void) {
    printf("Starting buddy test\n");

    printf("\nallocating 1024-byte block\n");
    void *e = buddy_alloc(1000);
    buddy_print(e);

    printf("\nallocating 128-byte block\n");
    void *c = buddy_alloc(112);
    buddy_print(c);

    printf("\nallocating 32-byte block\n");
    void *a = buddy_alloc(16);
    buddy_print(a);

    printf("\nfreeing 1024-byte block\n");
    buddy_free(e);
    buddy_print(a);

    printf("\nallocating 128-byte block\n");
    void *b = buddy_alloc(112);
    buddy_print(b);

    printf("\nfreeing 32-byte block\n");
    buddy_free(a);
    buddy_print(b);

    printf("\nfreeing first 128-byte block\n");
    buddy_free(c);
    buddy_print(b);

    printf("\nallocating 2048-byte block\n");
    void *d = buddy_alloc(2000);
    buddy_print(d);

    printf("\nfreeing other 128-byte block\n");
    buddy_free(b);
    buddy_print(d);

    printf("\nfreeing 2048-byte block\n");
    buddy_free(d);
}

void* buddy_alloc(uint64 length) {
    if (length == 0 || length > 4080) {
        return 0;
    }

    // Include header size
    uint64 total_size = length + sizeof(struct buddy_header);

    // Find the appropriate order
    int order = MIN_ORDER;
    while ((1UL << order) < total_size && order <= MAX_ORDER) {
        order++;
    }

    if (order > MAX_ORDER) {
        return 0; // Requested size too big
    }

    acquire(&buddy_lock);

    int current_order = order;
    struct buddy_header* block = NULL;

    // Step 1: Search for a free block in the appropriate free list or higher
    while (current_order <= MAX_ORDER) {
        if (free_lists[current_order - MIN_ORDER]) {
            // Found a free block
            block = free_lists[current_order - MIN_ORDER];
            // Remove it from the free list
            free_lists[current_order - MIN_ORDER] = block->next;
            block->next = NULL; // Clear next pointer for allocated block
            break;
        }
        current_order++;
    }

    // Step 2: If no block found, allocate a new 4096-byte block
    if (!block) {
        void* new_block = kalloc();
        if (!new_block) {
            release(&buddy_lock);
            return 0; // Out of memory
        }

        // Initialize the new block as a free block of MAX_ORDER
        block = (struct buddy_header*)new_block;
        block->magic = MAGIC_FREE;
        block->size = 1UL << MAX_ORDER;
        block->next = NULL;

        // Do not add the new block to the free list
        current_order = MAX_ORDER;
    }

    // Step 3: Split blocks until we reach the desired order
    while (current_order > order) {
        current_order--;
        uint64 split_size = 1UL << current_order;

        // Split the block into two buddies
        struct buddy_header* buddy = (struct buddy_header*)((char*)block + split_size);

        // Initialize the buddy block as a free block
        buddy->magic = MAGIC_FREE;
        buddy->size = split_size;
        buddy->next = free_lists[current_order - MIN_ORDER];
        free_lists[current_order - MIN_ORDER] = buddy;

        // Adjust the original block
        block->size = split_size;
    }

    // Step 4: Mark the block as allocated
    block->magic = MAGIC_ALLOCATED;

    release(&buddy_lock);

    // Return pointer to usable memory (after the header)
    return (void *)((char *)block + sizeof(struct buddy_header));
}

void buddy_free(void *ptr) {
    if (!ptr) {
        return;
    }

    // Get the block header
    struct buddy_header* block = (struct buddy_header*)((char*)ptr - sizeof(struct buddy_header));

    acquire(&buddy_lock);

    // Validate the block
    if (block->magic != MAGIC_ALLOCATED) {
        panic("buddy_free: invalid magic number");
    }

    if (block->size < (1UL << MIN_ORDER) || block->size > (1UL << MAX_ORDER)) {
        panic("buddy_free: invalid block size");
    }

    if (((uint64)block) & (block->size - 1)) {
        panic("buddy_free: block not properly aligned");
    }

    // Mark the block as free
    block->magic = MAGIC_FREE;

    int order = size_to_order(block->size);

    // Coalesce with buddy if possible
    while (order < MAX_ORDER) {
        struct buddy_header* buddy = find_buddy(block);

        // Check if buddy is free and has the same size
        struct buddy_header** list = &free_lists[order - MIN_ORDER];
        struct buddy_header* prev = NULL;
        struct buddy_header* curr = *list;
        int buddy_found = 0;

        while (curr) {
            if (curr == buddy && curr->magic == MAGIC_FREE) {
                // Remove buddy from free list
                if (prev) {
                    prev->next = curr->next;
                } else {
                    *list = curr->next;
                }
                buddy_found = 1;
                break;
            }
            prev = curr;
            curr = curr->next;
        }

        if (buddy_found) {
            // Merge the two blocks
            if ((uint64)block > (uint64)buddy) {
                // Ensure block has lower address
                struct buddy_header* temp = block;
                block = buddy;
                buddy = temp;
            }
            block->size *= 2;
            order++;
        } else {
            break; // Can't coalesce further
        }
    }

    if (block->size == (1UL << MAX_ORDER)) {
        // Return the block to kfree
        kfree((void*)block);
    } else {
        // Add the block to the appropriate free list
        // Keep the list in memory order
        struct buddy_header** list = &free_lists[order - MIN_ORDER];
        struct buddy_header* prev = NULL;
        struct buddy_header* curr = *list;

        while (curr && (uint64)curr < (uint64)block) {
            prev = curr;
            curr = curr->next;
        }

        block->next = curr;
        if (prev) {
            prev->next = block;
        } else {
            *list = block;
        }
    }

    release(&buddy_lock);
}
