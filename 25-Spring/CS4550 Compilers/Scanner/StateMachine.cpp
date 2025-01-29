#include "StateMachine.h"
#include <cctype> // For isalpha, isdigit, isspace
#include <iostream>
#include <cstdlib> // For exit

StateMachineClass::StateMachineClass() {
    // Initialize the current state
    mCurrentState = START_STATE;

    // Initialize all transitions to CANTMOVE_STATE
    for (int i = 0; i < LAST_STATE; i++) {
        for (int j = 0; j < LAST_CHAR; j++) {
            mLegalMoves[i][j] = CANTMOVE_STATE;
        }
    }

    // Define legal moves based on the DFA
    mLegalMoves[START_STATE][WHITESPACE_CHAR] = START_STATE;
    mLegalMoves[START_STATE][LETTER_CHAR] = IDENTIFIER_STATE;
        // Once we're in IDENTIFIER_STATE, we should remain there upon seeing more letters/digits/underscores.
    mLegalMoves[IDENTIFIER_STATE][LETTER_CHAR] = IDENTIFIER_STATE;
    mLegalMoves[IDENTIFIER_STATE][DIGIT_CHAR] = IDENTIFIER_STATE;
        // If you allow underscores in identifiers, either treat them as LETTER_CHAR or make a separate rule.
    mLegalMoves[START_STATE][DIGIT_CHAR] = INTEGER_STATE;
        // Once in INTEGER_STATE, remain there if we see another digit.
    mLegalMoves[INTEGER_STATE][DIGIT_CHAR] = INTEGER_STATE;
    mLegalMoves[START_STATE][PLUS_CHAR] = PLUS_STATE;
    mLegalMoves[START_STATE][MINUS_CHAR] = MINUS_STATE;
    mLegalMoves[START_STATE][TIMES_CHAR] = TIMES_STATE;
    mLegalMoves[START_STATE][DIVIDE_CHAR] = DIVIDE_STATE;
    mLegalMoves[START_STATE][LPAREN_CHAR] = LPAREN_STATE;
    mLegalMoves[START_STATE][RPAREN_CHAR] = RPAREN_STATE;
    mLegalMoves[START_STATE][SEMICOLON_CHAR] = SEMICOLON_STATE;
    mLegalMoves[START_STATE][LCURLY_CHAR] = LCURLY_STATE;
    mLegalMoves[START_STATE][RCURLY_CHAR] = RCURLY_STATE;
    mLegalMoves[START_STATE][EQUAL_CHAR] = ASSIGNMENT_STATE;
    mLegalMoves[START_STATE][LESS_CHAR] = LESS_STATE;
    mLegalMoves[START_STATE][GREATER_CHAR] = GREATER_STATE;
    mLegalMoves[START_STATE][NOT_CHAR] = NOTEQUAL_STATE;
    mLegalMoves[START_STATE][ENDFILE_CHAR] = ENDFILE_STATE;

    // Add transitions for multi-character operators
    mLegalMoves[LESS_STATE][EQUAL_CHAR] = LESSEQUAL_STATE;
    mLegalMoves[LESS_STATE][LESS_CHAR] = INSERTION_STATE;
    mLegalMoves[GREATER_STATE][EQUAL_CHAR] = GREATEREQUAL_STATE;
    mLegalMoves[NOTEQUAL_STATE][EQUAL_CHAR] = NOTEQUAL_STATE;

    // Initialize corresponding token types to BAD_TOKEN
    for (int i = 0; i < LAST_STATE; i++) {
        mCorrespondingTokenTypes[i] = BAD_TOKEN;
    }

    // Map final states to their token types
    mCorrespondingTokenTypes[IDENTIFIER_STATE] = IDENTIFIER_TOKEN;
    mCorrespondingTokenTypes[INTEGER_STATE] = INTEGER_TOKEN;
    mCorrespondingTokenTypes[PLUS_STATE] = PLUS_TOKEN;
    mCorrespondingTokenTypes[MINUS_STATE] = MINUS_TOKEN;
    mCorrespondingTokenTypes[TIMES_STATE] = TIMES_TOKEN;
    mCorrespondingTokenTypes[DIVIDE_STATE] = DIVIDE_TOKEN;
    mCorrespondingTokenTypes[LPAREN_STATE] = LPAREN_TOKEN;
    mCorrespondingTokenTypes[RPAREN_STATE] = RPAREN_TOKEN;
    mCorrespondingTokenTypes[SEMICOLON_STATE] = SEMICOLON_TOKEN;
    mCorrespondingTokenTypes[LCURLY_STATE] = LCURLY_TOKEN;
    mCorrespondingTokenTypes[RCURLY_STATE] = RCURLY_TOKEN;
    mCorrespondingTokenTypes[ASSIGNMENT_STATE] = ASSIGNMENT_TOKEN;
    mCorrespondingTokenTypes[LESS_STATE] = LESS_TOKEN;
    mCorrespondingTokenTypes[LESSEQUAL_STATE] = LESSEQUAL_TOKEN;
    mCorrespondingTokenTypes[INSERTION_STATE] = INSERTION_TOKEN;
    mCorrespondingTokenTypes[GREATER_STATE] = GREATER_TOKEN;
    mCorrespondingTokenTypes[GREATEREQUAL_STATE] = GREATEREQUAL_TOKEN;
    mCorrespondingTokenTypes[NOTEQUAL_STATE] = NOTEQUAL_TOKEN;
    mCorrespondingTokenTypes[ENDFILE_STATE] = ENDFILE_TOKEN;
}

// Helper to convert a character into its CharacterType
CharacterType StateMachineClass::GetCharacterType(char c) {
    if (c == EOF) return ENDFILE_CHAR;
    if (isalpha(c) || c == '_') return LETTER_CHAR;
    if (isdigit(c)) return DIGIT_CHAR;
    if (isspace(c)) return WHITESPACE_CHAR;
    switch (c) {
        case '+': return PLUS_CHAR;
        case '-': return MINUS_CHAR;
        case '*': return TIMES_CHAR;
        case '/': return DIVIDE_CHAR;
        case '(': return LPAREN_CHAR;
        case ')': return RPAREN_CHAR;
        case ';': return SEMICOLON_CHAR;
        case '{': return LCURLY_CHAR;
        case '}': return RCURLY_CHAR;
        case '=': return EQUAL_CHAR;
        case '<': return LESS_CHAR;
        case '>': return GREATER_CHAR;
        case '!': return NOT_CHAR;
        default: return BAD_CHAR;
    }
}

// Update the state machine based on the current character
MachineState StateMachineClass::UpdateState(char currentCharacter, TokenType &previousTokenType) {
    CharacterType charType = GetCharacterType(currentCharacter);

    // Save the token type associated with the current state
    previousTokenType = mCorrespondingTokenTypes[mCurrentState];

    // Update the current state based on the input character type
    mCurrentState = mLegalMoves[mCurrentState][charType];

    return mCurrentState;
}
