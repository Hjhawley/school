#include <iostream>
#include "Symbol.h"
#include "Scanner.h"
#include "Token.h"

void testScanner() {
    std::cout << "----- Scanner Test -----\n";
    
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
        std::cerr << "Error (Scanner): " << e.what() << std::endl;
        std::exit(1);
    }
}

void testSymbolTable() {
    std::cout << "\n----- Symbol Table Test -----\n";
    
    SymbolTableClass symbolTable;

    symbolTable.AddEntry("x");
    symbolTable.AddEntry("y");

    std::cout << "Symbol count: " << symbolTable.GetCount() << std::endl;  // Expected: 2

    std::cout << "Exists 'x'? " << (symbolTable.Exists("x") ? "true" : "false") << std::endl;  // Expected: true
    std::cout << "Exists 'z'? " << (symbolTable.Exists("z") ? "true" : "false") << std::endl;  // Expected: false

    std::cout << "Index of 'x': " << symbolTable.GetIndex("x") << std::endl;   // Expected: 0
    std::cout << "Index of 'y': " << symbolTable.GetIndex("y") << std::endl;   // Expected: 1

    std::cout << "Value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 0
    symbolTable.SetValue("x", 42);
    std::cout << "New value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 42

    // Uncomment these to test error handling
    // symbolTable.AddEntry("x");         // Should print an error and exit.
    // symbolTable.GetValue("z");         // Should print an error and exit.
    // symbolTable.SetValue("z", 10);       // Should print an error and exit.
}

int main() {
    testScanner();
    testSymbolTable();
    return 0;
}
