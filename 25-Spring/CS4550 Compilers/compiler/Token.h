#pragma once

#include <string>
#include <iostream>

enum TokenType {
	// Reserved keywords:
	VOID_TOKEN, MAIN_TOKEN, INT_TOKEN, COUT_TOKEN, IF_TOKEN, WHILE_TOKEN,
	// Relational operators:
	LESS_TOKEN, LESSEQUAL_TOKEN, GREATER_TOKEN, GREATEREQUAL_TOKEN,
	EQUAL_TOKEN, NOTEQUAL_TOKEN,
	// Other operators:
	INSERTION_TOKEN, ASSIGNMENT_TOKEN, PLUS_TOKEN, MINUS_TOKEN,
	TIMES_TOKEN, DIVIDE_TOKEN,
	// Other characters:
	SEMICOLON_TOKEN, LPAREN_TOKEN, RPAREN_TOKEN, LCURLY_TOKEN,
	RCURLY_TOKEN,
    // Logic
    AND_TOKEN, OR_TOKEN,
	// Other token types:
	IDENTIFIER_TOKEN, INTEGER_TOKEN,
	BAD_TOKEN, ENDFILE_TOKEN
};

// IMPORTANT: The list above and the list below MUST be kept in sync.
const std::string gTokenTypeNames[] = {
"VOID", "MAIN", "INT", "COUT", "IF", "WHILE",
"LESS", "LESSEQUAL", "GREATER", "GREATEREQUAL", "EQUAL",
"NOTEQUAL",
"INSERTION", "ASSIGNMENT", "PLUS", "MINUS", "TIMES", "DIVIDE",
"SEMICOLON", "LPAREN", "RPAREN", "LCURLY", "RCURLY",
"AND", "OR",
"IDENTIFIER", "INTEGER",
"BAD", "ENDFILE"
};

class TokenClass {
private:
    TokenType mType;
    std::string mLexeme;

public:
    // Constructor
    TokenClass(TokenType type, const std::string &lexeme);

    // Accessors
    TokenType GetTokenType() const { return mType; }
    const std::string& GetTokenTypeName() const {
        return gTokenTypeNames[mType];
    }
    std::string GetLexeme() const { return mLexeme; }

    // A static helper to get a name from any TokenType
    static const std::string& GetTokenTypeName(TokenType type) {
        return gTokenTypeNames[type];
    }
};

// Insertion operator prototype
std::ostream& operator<<(std::ostream &out, const TokenClass &tc);