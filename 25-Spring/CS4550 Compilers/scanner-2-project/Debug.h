#pragma once
#include <iostream>

// Set 1 to enable debug messages, 0 to disable
#define ShowMessages 0

#if ShowMessages
    #define MSG(X) std::cout << X << std::endl
#else
    #define MSG(X)
#endif
