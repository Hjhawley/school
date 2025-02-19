#include <iostream>
#include "Symbol.h"
// #include "Scanner.h" // Temporarily comment out if you don't want to run the scanner
// #include "Token.h"   // Temporarily comment out if you don't want to run the scanner

int main() {
    // -------------------------------------------------
    // 1) Symbol Table Testing
    // -------------------------------------------------
    SymbolTableClass symbolTable;

    // Add entries.
    symbolTable.AddEntry("x");
    symbolTable.AddEntry("y");

    // Test GetCount.
    std::cout << "Symbol count: " << symbolTable.GetCount() << std::endl;  // Expected: 2

    // Test Exists.
    std::cout << "Exists 'x'? " << (symbolTable.Exists("x") ? "true" : "false") << std::endl;  // true
    std::cout << "Exists 'z'? " << (symbolTable.Exists("z") ? "true" : "false") << std::endl;  // false

    // Test GetIndex.
    std::cout << "Index of 'x': " << symbolTable.GetIndex("x") << std::endl;   // e.g., 0
    std::cout << "Index of 'y': " << symbolTable.GetIndex("y") << std::endl;   // e.g., 1

    // Test GetValue and SetValue.
    std::cout << "Value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 0
    symbolTable.SetValue("x", 42);
    std::cout << "New value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 42

    // Uncomment the following lines one at a time to test error handling:
    // symbolTable.AddEntry("x");         // Should print an error and exit.
    // symbolTable.GetValue("z");         // Should print an error and exit.
    // symbolTable.SetValue("z", 10);     // Should print an error and exit.

    // -------------------------------------------------
    // 2) (Optional) Put Your Scanner Code Back In
    // -------------------------------------------------
    /*
    const std::string inputFileName = "code.txt";
    ScannerClass scanner(inputFileName);
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
    */

    return 0;
}
