#include "types.h"
#include "spinlock.h"
#include "defs.h"
#include "memlayout.h"
#include "param.h"

#define MIN_BLOCK_SIZE 32
#define MAX_BLOCK_SIZE 4096
#define NUM_FREE_LISTS 8

#define ALLOC_MAGIC 0xabcdefabcdefabcdULL
#define FREE_MAGIC  0x1234567890abcdefULL

struct {
    struct spinlock lock;
    void *freelist[NUM_FREE_LISTS];  // Array of free lists for each block size
} buddy;

// Header structure for both allocated and free blocks
typedef struct {
    uint64 magic;  // Magic number to mark used or free block
    uint64 size;   // Total size of the block including the header
} header_t;

// Initialize the buddy allocator (already implemented in buddyinit)
void
buddyinit(void)
{
    initlock(&buddy.lock, "buddylock");
    for (int i = 0; i < NUM_FREE_LISTS; i++) {
        buddy.freelist[i] = 0;
    }
}

// Helper function to find the index in freelist for a given size
int
size_to_index(uint64 size)
{
    int index = 0;
    uint64 s = MIN_BLOCK_SIZE;
    while (s < size && index < NUM_FREE_LISTS) {
        s <<= 1;
        index++;
    }
    return index;
}

// Allocate a single block of memory at least as big as the requested size
void*
buddy_alloc(uint64 length)
{
    if (length == 0 || length > 4080) {
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

        // First half
        void *first_half = block_to_split;
        header_t *first_hdr = (header_t *)first_half;
        first_hdr->magic = FREE_MAGIC;
        first_hdr->size = split_size;

        // Second half
        void *second_half = (char *)block_to_split + split_size;
        header_t *second_hdr = (header_t *)second_half;
        second_hdr->magic = FREE_MAGIC;
        second_hdr->size = split_size;

        // Add the second half to the free list of the smaller size
        int split_index = i - 1;
        void **second_next_ptr = (void **)((char *)second_half + sizeof(header_t));
        *second_next_ptr = buddy.freelist[split_index];
        buddy.freelist[split_index] = second_half;

        // Prepare to split the first half in the next iteration
        block = first_half;
        i--;
    }

    // Allocate the block
    header_t *hdr = (header_t *)block;
    hdr->magic = ALLOC_MAGIC;
    hdr->size = size;

    // Remove block from the free list
    void **next_ptr = (void **)((char *)block + sizeof(header_t));
    buddy.freelist[index] = *next_ptr;

    release(&buddy.lock);

    // Return a pointer to the usable space
    return (void *)((char *)block + sizeof(header_t));
}
