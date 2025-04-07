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
    MachineState currentState;      // Current state of the DFA
    TokenType previousTokenType;    // The token type associated with the previous state

    // Read characters and update the DFA state
    do {
        char c = mFin.get(); // Read the next character
        lexeme.push_back(c); // Append it to the lexeme

        // Update the DFA state
        currentState = stateMachine.UpdateState(c, previousTokenType);

        // If we read a newline, increment the line number
        if (c == '\n') {
            mLineNumber++;
        }

        // If the state resets (e.g., due to whitespace), clear the lexeme
        if (currentState == START_STATE || currentState == ENDFILE_STATE) {
            lexeme.clear();
        }
    } while (currentState != CANTMOVE_STATE); // Continue until no valid transition exists

    // The last character read caused CANT_MOVE. Remove it from the lexeme
    // If that character is a newline, it will be re-read later so decrement the line count
    // to avoid double counting
    if (!lexeme.empty() && lexeme.back() == '\n') {
        mLineNumber--;
    }
    lexeme.pop_back();
    mFin.unget(); // Put the last character back into the input stream

    // If the token type is BAD_TOKEN, report an error and exit
    if (previousTokenType == BAD_TOKEN) {
        std::cerr << "Error: BAD_TOKEN from lexeme \"" << lexeme << "\"" << std::endl;
        std::exit(1);
    }

    // Create a TokenClass object with the lexeme and token type
    TokenClass token(previousTokenType, lexeme);
    MSG("Returning token: ");
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

    // Return the token we got
    return tc;
}

