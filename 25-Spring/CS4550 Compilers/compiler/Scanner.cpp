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

    StateMachineClass stateMachine; // Instance of the DFA
    std::string lexeme;             // Stores the current token lexeme
    MachineState currentState = START_STATE;  // Ensure initialized
    TokenType previousTokenType = BAD_TOKEN;  // Start with BAD

    while (true) {
        // Check for end-of-file before reading
        if (mFin.peek() == EOF) {
            return TokenClass(ENDFILE_TOKEN, "EOF");
        }

        char c = mFin.get();
        lexeme.push_back(c);

        currentState = stateMachine.UpdateState(c, previousTokenType);

        if (c == '\n') {
            mLineNumber++;
        }

        // If the state machine resets, we clear and keep scanning
        if (currentState == START_STATE || currentState == ENDFILE_STATE) {
            lexeme.clear();
            continue;
        }

        if (currentState == CANTMOVE_STATE) {
            break;
        }
    }

    // Back up one character (which caused failure)
    if (!lexeme.empty()) {
        if (lexeme.back() == '\n') {
            mLineNumber--;
        }
        lexeme.pop_back();
        mFin.unget();
    }

    // If we got nothing valid, return EOF
    if (lexeme.empty()) {
        return TokenClass(ENDFILE_TOKEN, "EOF");
    }

    if (previousTokenType == BAD_TOKEN) {
        std::cerr << "Error: BAD_TOKEN from lexeme \"" << lexeme << "\"" << std::endl;
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
