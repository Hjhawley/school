#pragma once

#include "Token.h" // For TokenType

// Enum for the machine states
enum MachineState {
    START_STATE,
    IDENTIFIER_STATE,
    INTEGER_STATE,
    PLUS_STATE,
    MINUS_STATE,
    TIMES_STATE,
    DIVIDE_STATE,
    LINE_COMMENT_STATE,
    BLOCK_COMMENT_1_STATE,
    BLOCK_COMMENT_2_STATE,
    LPAREN_STATE,
    RPAREN_STATE,
    SEMICOLON_STATE,
    LCURLY_STATE,
    RCURLY_STATE,
    ASSIGNMENT_STATE,
    LESS_STATE,
    LESSEQUAL_STATE,
    INSERTION_STATE,
    GREATER_STATE,
    GREATEREQUAL_STATE,
    NOTEQUAL_STATE,
    ENDFILE_STATE,
    CANTMOVE_STATE, // State when there's no valid transition
    LAST_STATE      // Not an actual state; just represents the count
};

// Enum for character types
enum CharacterType {
    LETTER_CHAR,
    DIGIT_CHAR,
    WHITESPACE_CHAR, // space, tab
    RETURN_CHAR,     // newline (\n)
    PLUS_CHAR,
    MINUS_CHAR,
    TIMES_CHAR,
    DIVIDE_CHAR,
    LPAREN_CHAR,
    RPAREN_CHAR,
    SEMICOLON_CHAR,
    LCURLY_CHAR,
    RCURLY_CHAR,
    EQUAL_CHAR,
    LESS_CHAR,
    GREATER_CHAR,
    NOT_CHAR,
    ENDFILE_CHAR,
    BAD_CHAR, // For invalid input
    LAST_CHAR // Not an actual type; just represents the count
};

// The state machine class
class StateMachineClass {
public:
    StateMachineClass();
    MachineState UpdateState(char currentCharacter, TokenType &previousTokenType);

private:
    MachineState mCurrentState;
    MachineState mLegalMoves[LAST_STATE][LAST_CHAR]; // Transition table
    TokenType mCorrespondingTokenTypes[LAST_STATE]; // Maps states to token types

    CharacterType GetCharacterType(char c); // Helper to categorize input
};
