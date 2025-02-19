#include <iostream>
#include "Symbol.h"
#include "Scanner.h"
#include "Token.h"

int main() {
    // Scanner testing
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

    // Symbol Table Testing
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
    std::cout << "Index of 'x': " << symbolTable.GetIndex("x") << std::endl;   // 0
    std::cout << "Index of 'y': " << symbolTable.GetIndex("y") << std::endl;   // 1

    // Test GetValue and SetValue.
    std::cout << "Value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 0
    symbolTable.SetValue("x", 42);
    std::cout << "New value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 42

    // These should all throw an error and exit:
    // symbolTable.AddEntry("x");
    // symbolTable.GetValue("z");
    // symbolTable.SetValue("z", 10);

    return 0;
}
