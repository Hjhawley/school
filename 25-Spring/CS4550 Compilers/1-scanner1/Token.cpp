#include "Token.h"
#include <iostream>

// The constructor initializes mType, mLexeme, then checks if the lexeme is a reserved word:
TokenClass::TokenClass(TokenType type, const std::string &lexeme)
    : mType(type), mLexeme(lexeme)
{
    // If it's an IDENTIFIER_TOKEN initially, check if it matches a reserved word:
    if (mType == IDENTIFIER_TOKEN) {
        if (lexeme == "void") {
            mType = VOID_TOKEN;
        }
        else if (lexeme == "main") {
            mType = MAIN_TOKEN;
        }
        else if (lexeme == "int") {
            mType = INT_TOKEN;
        }
        else if (lexeme == "cout") {
            mType = COUT_TOKEN;
        }
    }
}

// The insertion operator for printing a token
std::ostream& operator<<(std::ostream &out, const TokenClass &tc) {
    out << tc.GetTokenTypeName()
        << " (\"" << tc.GetLexeme() << "\")";
    return out;
}
