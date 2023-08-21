#ifndef _DEBUGGER_H_
#define _DEBUGGER_H_
#include <iostream>

#if DEBUG_LEVEL > 3

#define FILE_LINE __FILE__ << ":" << __LINE__ << " "
#define DEBUG_MESSAGE(msg) std::cout << FILE_LINE << msg << std::endl

#elif DEBUG_LEVEL > 1

#define DEBUG_MESSAGE(msg) std::cout << msg << std::endl

#else

#define DEBUG_MESSAGE(msg)

#endif // DEBUG_LEVEL

#endif /* _DEBUGGER_H_ */
/* Local Variables: */
/* mode:c++         */
/* End:             */
