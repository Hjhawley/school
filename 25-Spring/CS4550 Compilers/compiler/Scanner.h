#pragma once

#include <fstream>
#include "StateMachine.h"
#include "Token.h"

class ScannerClass {
public:
    // Constructor: opens the input file and initializes the line number to 1
    ScannerClass(const std::string &inputFileName);

    // Destructor: closes the input file
    ~ScannerClass();

    // Reads the next token from the file and returns it
    TokenClass GetNextToken();

    TokenClass PeekNextToken();

    // Accessor for the current line number
    int GetLineNumber() const { return mLineNumber; }

private:
    std::ifstream mFin; // Input file stream
    int mLineNumber;    // Tracks the current line number
};
