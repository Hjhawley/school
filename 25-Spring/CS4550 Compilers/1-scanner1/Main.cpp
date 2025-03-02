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
        // Repeatedly call GetNextToken and print each token
        do {
            TokenClass tc = scanner.GetNextToken();
            std::cout << tc << std::endl; // Print the token using the overloaded << operator
            tt = tc.GetTokenType();       // Update the token type for the loop condition
        } while (tt != ENDFILE_TOKEN);    // Stop when we reach the end of the file
    }
    catch (const std::exception &e) {
        // Catch any exceptions thrown (optional)
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
