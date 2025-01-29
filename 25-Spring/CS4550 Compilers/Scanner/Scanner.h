#pragma once

#include <fstream> // For file handling
#include "StateMachine.h" // For StateMachineClass, TokenType, etc.
#include "Token.h" // For TokenClass

class ScannerClass {
public:
    // Constructor: opens the input file
    ScannerClass(const std::string &inputFileName);

    // Destructor: closes the input file
    ~ScannerClass();

    // Reads the next token from the file and returns it
    TokenClass GetNextToken();

private:
    std::ifstream mFin; // Input file stream
};
