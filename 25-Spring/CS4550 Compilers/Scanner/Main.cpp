#include <iostream>
#include "Scanner.h"

int main() {
    ScannerClass scanner("code.txt");

    TokenClass token;
    do {
        token = scanner.GetNextToken();
        std::cout << token << std::endl; // Print the token
    } while (token.GetTokenType() != ENDFILE_TOKEN);

    return 0;
}
