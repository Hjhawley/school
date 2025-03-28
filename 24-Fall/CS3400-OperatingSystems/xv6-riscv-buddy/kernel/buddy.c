#include "types.h"
#include "riscv.h"
#include "spinlock.h"
#include "defs.h"
#include "memlayout.h"
#include "param.h"

#define MIN_BLOCK_SIZE 32
#define MAX_BLOCK_SIZE 4096
#define NUM_FREE_LISTS 8 // not 7?

#define ALLOC_MAGIC 0xabcdefabcdefabcdULL
#define FREE_MAGIC  0x1234567890abcdefULL

extern char end[];

struct {
    struct spinlock lock;
    void *freelist[NUM_FREE_LISTS];  // Array of free lists for each block size
} buddy;

// Header structure for both allocated and free blocks
typedef struct header_t {
    uint64 magic;
    uint64 size;
} header_t;

void
buddyinit(void)
{
    initlock(&buddy.lock, "buddylock");
    for (int i = 0; i < NUM_FREE_LISTS; i++) {
        buddy.freelist[i] = 0;
    }
}

// find the index in freelist for a given size
int
size_to_index(uint64 size)
{
    int index = 0;
    uint64 s = MIN_BLOCK_SIZE;
    while (s < size && index < NUM_FREE_LISTS - 1) {
        s <<= 1;
        index++;
    }
    return index;
}

// check if a block is in the free list
int
is_block_free(void *block_addr, uint64 size)
{
    int index = size_to_index(size);
    if (index >= NUM_FREE_LISTS) {
        return 0;
    }
    void *cur = buddy.freelist[index];
    while (cur) {
        if (cur == block_addr) {
            return 1;  // Block is free
        }
        // Move to the next block in the free list
        cur = *(void **)((char *)cur + sizeof(header_t));
    }
    return 0;  // Block is not free
}

// Allocate a single block of memory at least as big as the requested size
void*
buddy_alloc(uint64 length)
{
    if (length == 0 || length > (MAX_BLOCK_SIZE - sizeof(header_t))) {
        return 0;  // Return zero for invalid requests
    }

    acquire(&buddy.lock);

    // Calculate the total size needed including the header
    uint64 total_size = length + sizeof(header_t);

    // Find the smallest power of two block size that fits the total_size
    uint64 size = MIN_BLOCK_SIZE;
    int index = 0;
    while (size < total_size && size < MAX_BLOCK_SIZE) {
        size <<= 1;
        index++;
    }

    if (size > MAX_BLOCK_SIZE) {
        release(&buddy.lock);
        return 0;  // Cannot allocate blocks larger than MAX_BLOCK_SIZE
    }

    // Try to find a block of the appropriate size
    void *block = buddy.freelist[index];
    if (block) {
        // Remove block from the free list
        void **next_ptr = (void **)((char *)block + sizeof(header_t));
        buddy.freelist[index] = *next_ptr;

        // Set up the allocated block header
        header_t *hdr = (header_t *)block;
        hdr->magic = ALLOC_MAGIC;
        hdr->size = size;

        release(&buddy.lock);
        // Return a pointer to the usable space (after the header)
        return (void *)((char *)block + sizeof(header_t));
    }

    // No free block of the required size, need to split larger blocks
    int i;
    for (i = index + 1; i < NUM_FREE_LISTS; i++) {
        if (buddy.freelist[i]) {
            break;
        }
    }

    // If no larger block is available, allocate a new one using kalloc
    if (i == NUM_FREE_LISTS) {
        void *new_block = kalloc();
        if (!new_block) {
            release(&buddy.lock);
            return 0;  // Allocation failed
        }
        // Initialize the new block as a free block of maximum size
        header_t *hdr = (header_t *)new_block;
        hdr->magic = FREE_MAGIC;
        hdr->size = MAX_BLOCK_SIZE;

        // Add the new block to the largest free list
        void **next_ptr = (void **)((char *)new_block + sizeof(header_t));
        *next_ptr = buddy.freelist[NUM_FREE_LISTS - 1];
        buddy.freelist[NUM_FREE_LISTS - 1] = new_block;
        i = NUM_FREE_LISTS - 1;  // Update index to the largest block size
    }

    // Split larger blocks until we get a block of the desired size
    while (i > index) {
        // Remove block from the current free list
        void *block_to_split = buddy.freelist[i];
        void **next_ptr = (void **)((char *)block_to_split + sizeof(header_t));
        buddy.freelist[i] = *next_ptr;

        // Split the block into two halves
        uint64 split_size = ((header_t *)block_to_split)->size / 2;

        void *first_half = block_to_split;
        header_t *first_hdr = (header_t *)first_half;
        first_hdr->magic = FREE_MAGIC;
        first_hdr->size = split_size;

        void *second_half = (char *)block_to_split + split_size;
        header_t *second_hdr = (header_t *)second_half;
        second_hdr->magic = FREE_MAGIC;
        second_hdr->size = split_size;

        // Add both halves to the free list of the smaller size
        int split_index = i - 1;

        void **first_next_ptr = (void **)((char *)first_half + sizeof(header_t));
        *first_next_ptr = buddy.freelist[split_index];
        buddy.freelist[split_index] = first_half;

        void **second_next_ptr = (void **)((char *)second_half + sizeof(header_t));
        *second_next_ptr = buddy.freelist[split_index];
        buddy.freelist[split_index] = second_half;

        i--;
    }

    // Now allocate the block from the free list
    block = buddy.freelist[index];
    if (block == 0) {
        release(&buddy.lock);
        return 0;  // Shouldn't happen?
    }

    // Remove block from the free list
    void **next_ptr = (void **)((char *)block + sizeof(header_t));
    buddy.freelist[index] = *next_ptr;

    // Set up the allocated block header
    header_t *hdr = (header_t *)block;
    hdr->magic = ALLOC_MAGIC;
    hdr->size = size;

    release(&buddy.lock);

    // Return a pointer to the usable space
    return (void *)((char *)block + sizeof(header_t));
}

// check if a number is a power of two
int
is_power_of_two(uint64 x)
{
    return (x != 0) && ((x & (x - 1)) == 0);
}

// Free a previously allocated block
void
buddy_free(void *ptr)
{
    if (ptr == 0) {
        return;
    }

    acquire(&buddy.lock);

    // Get the header of the block
    header_t *hdr = (header_t *)((char *)ptr - sizeof(header_t));

    // Validate the magic number
    if (hdr->magic != ALLOC_MAGIC) {
        release(&buddy.lock);  
        panic("buddy_free: invalid magic number");
    }

    uint64 size = hdr->size;

    // Validate the size (must be power of two and within valid range)
    if (!is_power_of_two(size) || size < MIN_BLOCK_SIZE || size > MAX_BLOCK_SIZE) {
        release(&buddy.lock);  
        panic("buddy_free: invalid block size");
    }

    // Validate alignment
    uint64 block_addr = (uint64)hdr;
    if (block_addr % size != 0) {
        release(&buddy.lock);  
        panic("buddy_free: block not properly aligned");
    }

    // Mark the block as free
    hdr->magic = FREE_MAGIC;

    uint64 current_size = size;
    header_t *current_block = hdr;

    // Coalesce (what a good word)
    while (current_size < MAX_BLOCK_SIZE) {
        
        // Calculate the buddy's address
        uint64 buddy_addr = block_addr ^ current_size;
        header_t *buddy_hdr = (header_t *)buddy_addr;

        // Check if buddy is valid and free
        if ((uint64)buddy_hdr < (uint64)end || (uint64)buddy_hdr >= PHYSTOP) {
            // Buddy address is invalid
            break;
        }

        if (buddy_hdr->magic != FREE_MAGIC || buddy_hdr->size != current_size) {
            // Buddy is not free or not the same size
            break;
        }

        // Remove buddy from the free list
        int index = size_to_index(current_size);
        if (index >= NUM_FREE_LISTS) {
            // Invalid index
            break;
        }
        void **prev = &buddy.freelist[index];
        void *cur = *prev;
        int found = 0;

        while (cur) {
            if (cur == (void *)buddy_hdr) {
                // Remove buddy from the free list
                *prev = *(void **)((char *)cur + sizeof(header_t));
                found = 1;
                break;
            }
            prev = (void **)((char *)cur + sizeof(header_t));
            cur = *prev;
        }

        if (!found) {
            // Buddy not found in free list, cannot coalesce
            break;
        }

        // Determine the new block address (lower of the two)
        if (block_addr > buddy_addr) {
            block_addr = buddy_addr;
            current_block = buddy_hdr;
        }

        // Update the size
        current_size <<= 1;
        current_block->size = current_size;

        // Update the header
        current_block->magic = FREE_MAGIC;
    }

    if (current_size == MAX_BLOCK_SIZE) {
        // Return the block to kfree
        release(&buddy.lock);
        kfree((void *)current_block);
        return;
    }

    // Insert the block into the free list, keeping it in memory order
    int index = size_to_index(current_size);
    if (index >= NUM_FREE_LISTS) {
        // Invalid index, cannot insert
        release(&buddy.lock);
        panic("buddy_free: invalid block size during insertion");
    }
    void **prev = &buddy.freelist[index];
    void *cur = *prev;

    while (cur && cur < (void *)current_block) {
        prev = (void **)((char *)cur + sizeof(header_t));
        cur = *prev;
    }

    // Insert the block into the list
    *(void **)((char *)current_block + sizeof(header_t)) = cur;
    *prev = current_block;

    release(&buddy.lock);
}

// Recursive function to print the block structure
void
print_block(void *block_addr, uint64 size, int indent)
{
    if (size < MIN_BLOCK_SIZE) {
        return;
    }

    // Prepare indentation
    for (int i = 0; i < indent; i++) {
        printf("    ");
    }

    acquire(&buddy.lock);

    // Check if the block is free
    int is_free = is_block_free(block_addr, size);

    // Check if the block is allocated
    header_t *hdr = (header_t *)block_addr;
    int is_allocated = 0;
    if (hdr->magic == ALLOC_MAGIC && hdr->size == size) {
        is_allocated = 1;
    }

    // Now, check if the block has been split
    int is_split = 0;
    if (!is_free && !is_allocated && size > MIN_BLOCK_SIZE) {
        // Check if either of the two sub-blocks are allocated or free
        void *first_half = block_addr;
        void *second_half = (char *)block_addr + size / 2;

        int first_free = is_block_free(first_half, size / 2);
        int second_free = is_block_free(second_half, size / 2);

        header_t *first_hdr = (header_t *)first_half;
        header_t *second_hdr = (header_t *)second_half;

        int first_allocated = (first_hdr->magic == ALLOC_MAGIC && first_hdr->size == size / 2);
        int second_allocated = (second_hdr->magic == ALLOC_MAGIC && second_hdr->size == size / 2);

        if (first_free || second_free || first_allocated || second_allocated) {
            is_split = 1;
        }
    }

    release(&buddy.lock);

    if (is_allocated) {
        printf("└──── used (%lu)\n", size);
    } else if (is_split) {
        printf("└──── \n");
        // Recursively print the two halves
        print_block(block_addr, size / 2, indent + 1);
        print_block((void *)((char *)block_addr + size / 2), size / 2, indent + 1);
    } else {
        printf("└──── free (%lu)\n", size);
    }
}

void
buddy_print(void *ptr)
{
    // Find the start address of the 4096-byte block containing ptr
    uint64 block_start_addr = (uint64)ptr & ~(MAX_BLOCK_SIZE - 1);
    void *block_start = (void *)block_start_addr;
    print_block(block_start, MAX_BLOCK_SIZE, 0);
}

// Function to test the buddy allocator
void
buddy_test(void)
{
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
