#include "Scanner.h"
#include "Debug.h"

#include <iostream>
#include <cstdlib>  // For std::exit

ScannerClass::ScannerClass(const std::string &inputFileName)
    : mLineNumber(1) // Initialize line number
{
    MSG("Initializing ScannerClass object...");
    // Open the file in binary mode
    mFin.open(inputFileName.c_str(), std::ios::binary);
    if (!mFin) {
        std::cerr << "Error opening input file " << inputFileName << std::endl;
        std::exit(1);
    }
}

ScannerClass::~ScannerClass() {
    // Close the file stream
    if (mFin.is_open()) {
        mFin.close();
    }
}

TokenClass ScannerClass::GetNextToken() {
    MSG("Scanning for the next token...");

    StateMachineClass stateMachine;
    std::string lexeme;
    MachineState currentState = START_STATE;
    TokenType previousTokenType = BAD_TOKEN;

    while (true) {
        if (mFin.peek() == EOF) {
            return TokenClass(ENDFILE_TOKEN, "EOF");
        }

        char c = mFin.get();
        MachineState nextState = stateMachine.UpdateState(c, previousTokenType);

        if (c == '\n') {
            mLineNumber++;
        }

        if (nextState == CANTMOVE_STATE) {
            mFin.unget();
            break;
        }

        if (nextState == START_STATE || nextState == ENDFILE_STATE) {
            lexeme.clear();
            continue;
        }

        currentState = nextState;
        lexeme.push_back(c);
    }

    if (!lexeme.empty() && lexeme.back() == '\n') {
        mLineNumber--;
    }

    if (previousTokenType == BAD_TOKEN) {
        std::cerr << "Lexical error on line " << mLineNumber
                  << ": invalid token \"" << lexeme << "\"" << std::endl;
        std::exit(1);
    }

    TokenClass token(previousTokenType, lexeme);
    MSG("Returning token: " << token << std::endl);
    return token;
}

TokenClass ScannerClass::PeekNextToken() {
    // Save the current "get" position
    std::streampos filePos = mFin.tellg();
    int oldLineNumber = mLineNumber;

    // Call GetNextToken()
    TokenClass tc = GetNextToken();

    // If we triggered EOF, we need to clear it before seeking back
    if (!mFin) {
        mFin.clear();
    }

    // Reset "get" position
    mFin.seekg(filePos);

    // Restore line number
    mLineNumber = oldLineNumber;

    return tc;
}
