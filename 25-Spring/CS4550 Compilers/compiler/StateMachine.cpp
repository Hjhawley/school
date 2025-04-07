#include "StateMachine.h"
#include "Debug.h"

#include <iostream>
#include <cctype>
#include <cstdlib>

StateMachineClass::StateMachineClass() {
    MSG("Initializing DFA...");

    mCurrentState = START_STATE;
    // Initialize all transitions to CANTMOVE_STATE by default
    for (int i = 0; i < LAST_STATE; i++) {
        for (int j = 0; j < LAST_CHAR; j++) {
            mLegalMoves[i][j] = CANTMOVE_STATE;
        }
    }

    // Define legal moves based on the DFA
    mLegalMoves[START_STATE][WHITESPACE_CHAR] = START_STATE;
    mLegalMoves[START_STATE][RETURN_CHAR] = START_STATE;
    // Stay in ID state as long as we keep seeing valid chars
    mLegalMoves[START_STATE][LETTER_CHAR] = IDENTIFIER_STATE;
    mLegalMoves[IDENTIFIER_STATE][LETTER_CHAR] = IDENTIFIER_STATE;
    mLegalMoves[IDENTIFIER_STATE][DIGIT_CHAR] = IDENTIFIER_STATE;
    // TODO: allow underscores as valid chars (but not as the first char)
    mLegalMoves[START_STATE][DIGIT_CHAR] = INTEGER_STATE;
    // Stay in integer state as long as we keep seeing valid digits
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
    // Multi-character operators
    mLegalMoves[LESS_STATE][EQUAL_CHAR] = LESSEQUAL_STATE;
    mLegalMoves[LESS_STATE][LESS_CHAR] = INSERTION_STATE;
    mLegalMoves[GREATER_STATE][EQUAL_CHAR] = GREATEREQUAL_STATE;
    mLegalMoves[NOTEQUAL_STATE][EQUAL_CHAR] = NOTEQUAL_STATE;
    // Comments
    mLegalMoves[DIVIDE_STATE][DIVIDE_CHAR] = LINE_COMMENT_STATE;
    mLegalMoves[DIVIDE_STATE][TIMES_CHAR] = BLOCK_COMMENT_1_STATE;
    // Logical operators
    mLegalMoves[START_STATE][AND_CHAR] = AND_STATE;
    mLegalMoves[AND_STATE][AND_CHAR] = CANTMOVE_STATE;  // accept &&
    mLegalMoves[START_STATE][OR_CHAR] = OR_STATE;
    mLegalMoves[OR_STATE][OR_CHAR] = CANTMOVE_STATE;    // accept ||

    // In a line comment, stay in the comment until we reach a newline or EOF
    for (int j = 0; j < LAST_CHAR; j++) {
        mLegalMoves[LINE_COMMENT_STATE][j] = LINE_COMMENT_STATE;
    }
    mLegalMoves[LINE_COMMENT_STATE][RETURN_CHAR] = START_STATE;
    mLegalMoves[LINE_COMMENT_STATE][ENDFILE_CHAR] = ENDFILE_STATE;
    // Start block comment when we see "/*" and stay until we see "*"
    for (int j = 0; j < LAST_CHAR; j++) {
        mLegalMoves[BLOCK_COMMENT_1_STATE][j] = BLOCK_COMMENT_1_STATE;
    }
    mLegalMoves[BLOCK_COMMENT_1_STATE][TIMES_CHAR] = BLOCK_COMMENT_2_STATE;
    for (int j = 0; j < LAST_CHAR; j++) {
        mLegalMoves[BLOCK_COMMENT_2_STATE][j] = BLOCK_COMMENT_1_STATE;
    }
    mLegalMoves[BLOCK_COMMENT_2_STATE][TIMES_CHAR] = BLOCK_COMMENT_2_STATE;
    mLegalMoves[BLOCK_COMMENT_2_STATE][DIVIDE_CHAR] = START_STATE;

    // Initialize token types to BAD_TOKEN by default
    for (int i = 0; i < LAST_STATE; i++) {
        mCorrespondingTokenTypes[i] = BAD_TOKEN;
    }
    // Map final states to token types
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
    mCorrespondingTokenTypes[AND_STATE] = AND_TOKEN;
    mCorrespondingTokenTypes[OR_STATE] = OR_TOKEN;
    mCorrespondingTokenTypes[ENDFILE_STATE] = ENDFILE_TOKEN;
    MSG("DFA initialized.");
}

// Helper to convert a character into its CharacterType
CharacterType StateMachineClass::GetCharacterType(char c) {
    if (c == EOF) return ENDFILE_CHAR;
    if (c == '\n') return RETURN_CHAR;
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
        case '&': return AND_CHAR;
        case '|': return OR_CHAR;
        default: return BAD_CHAR;
    }
}

// Update state machine based on the current character
MachineState StateMachineClass::UpdateState(char currentCharacter, TokenType &previousTokenType) {
    CharacterType charType = GetCharacterType(currentCharacter);

    // Save the token type associated with the current state
    previousTokenType = mCorrespondingTokenTypes[mCurrentState];

    // Update the current state based on the input character type
    mCurrentState = mLegalMoves[mCurrentState][charType];

    return mCurrentState;
}
