#include <iostream>
#include "Scanner.h" // Include ScannerClass and related headers
#include "Token.h"   // Include TokenClass for printing tokens

int main() {
    // Name of the source file containing the code to tokenize
    const std::string inputFileName = "code.txt";

    // Create the ScannerClass object, which will open the input file
    ScannerClass scanner(inputFileName);

    // TokenType variable to track the current token type
    TokenType tt;

    try {
        do {
            TokenClass tc = scanner.GetNextToken();
            std::cout << "Line " << scanner.GetLineNumber() << ": " << tc << std::endl;
            tt = tc.GetTokenType();
        } while (tt != ENDFILE_TOKEN);        
    }
    catch (const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
