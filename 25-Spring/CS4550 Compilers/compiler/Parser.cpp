#include "Parser.h"
#include "Debug.h"
#include <cstdlib>
#include <iostream>

ParserClass::ParserClass(ScannerClass *scanner, SymbolTableClass *symTable)
    : mScanner(scanner), mSymbolTable(symTable) {
}

// The top-level driver function (called by testParser())
void ParserClass::Start() {
    StartRule();
    std::cout << "Done parsing successfully!\n";
}

// <Start> → <Program> ENDFILE_TOKEN
void ParserClass::StartRule() {
    Program();
    Match(ENDFILE_TOKEN);
}

// <Program> → VOID MAIN LPAREN RPAREN <Block>
void ParserClass::Program() {
    Match(VOID_TOKEN);
    Match(MAIN_TOKEN);
    Match(LPAREN_TOKEN);
    Match(RPAREN_TOKEN);
    Block();
}

// <Block> → LCURLY_TOKEN <StatementGroup> RCURLY_TOKEN
void ParserClass::Block() {
    Match(LCURLY_TOKEN);
    StatementGroup();
    Match(RCURLY_TOKEN);
}

// <StatementGroup> → {empty} | <Statement> <StatementGroup>
void ParserClass::StatementGroup() {
    while (true) {
        // Peek token from the scanner:
        TokenType tt = mScanner->PeekNextToken().GetTokenType();

        // If we can't parse a statement, break
        if (!Statement()) {
            break;
        }
    }
}


// <Statement> -> <DeclarationStatement> | <AssignmentStatement> | <CoutStatement> | <Block>
bool ParserClass::Statement() {
    TokenType tt = mScanner->PeekNextToken().GetTokenType();

    if(tt == INT_TOKEN) {
        DeclarationStatement();
        return true;
    }
    else if(tt == IDENTIFIER_TOKEN) {
        AssignmentStatement();
        return true;
    }
    else if(tt == COUT_TOKEN) {
        CoutStatement();
        return true;
    }
    else if(tt == LCURLY_TOKEN) {
        Block(); // a block is also a Statement
        return true;
    }
    // If none matched, return false
    return false;
}

// <DeclarationStatement> → INT <Identifier> SEMICOLON
void ParserClass::DeclarationStatement() {
    Match(INT_TOKEN);
    Identifier();
    Match(SEMICOLON_TOKEN);
}

// <AssignmentStatement> → <Identifier> ASSIGNMENT <Expression> SEMICOLON
void ParserClass::AssignmentStatement() {
    Identifier();
    Match(ASSIGNMENT_TOKEN);
    Expression();
    Match(SEMICOLON_TOKEN);
}

// <CoutStatement> -> COUT INSERTION <Expression> SEMICOLON
void ParserClass::CoutStatement() {
    Match(COUT_TOKEN);
    Match(INSERTION_TOKEN); // '<<'
    Expression();
    Match(SEMICOLON_TOKEN);
}

// <Expression> -> <Relational>
void ParserClass::Expression() {
    Relational();
}

// <Relational> -> <PlusMinus> [one optional relational operator]
void ParserClass::Relational() {
    PlusMinus();
    TokenType tt = mScanner->PeekNextToken().GetTokenType();
    if(tt == LESS_TOKEN || tt == LESSEQUAL_TOKEN ||
       tt == GREATER_TOKEN || tt == GREATEREQUAL_TOKEN ||
       tt == EQUAL_TOKEN || tt == NOTEQUAL_TOKEN) {
        Match(tt);
        PlusMinus();
    }
}

// <PlusMinus> -> <TimesDivide> { plus/minus <TimesDivide> }
void ParserClass::PlusMinus() {
    TimesDivide();
    while(true) {
        TokenType tt = mScanner->PeekNextToken().GetTokenType();
        if(tt == PLUS_TOKEN || tt == MINUS_TOKEN) {
            Match(tt);
            TimesDivide();
        }
        else {
            return;
        }
    }
}

// <TimesDivide> -> <Factor> { times/divide <Factor> }
void ParserClass::TimesDivide() {
    Factor();
    while(true) {
        TokenType tt = mScanner->PeekNextToken().GetTokenType();
        if(tt == TIMES_TOKEN || tt == DIVIDE_TOKEN) {
            Match(tt);
            Factor();
        }
        else {
            return;
        }
    }
}

// <Factor> -> <Identifier> | <Integer> | LPAREN <Expression> RPAREN
void ParserClass::Factor() {
    TokenType tt = mScanner->PeekNextToken().GetTokenType();
    if(tt == IDENTIFIER_TOKEN) {
        Identifier();
    }
    else if(tt == INTEGER_TOKEN) {
        Integer();
    }
    else if(tt == LPAREN_TOKEN) {
        Match(LPAREN_TOKEN);
        Expression();
        Match(RPAREN_TOKEN);
    }
    else {
        std::cerr << "Error in Factor(): Expected IDENTIFIER, INTEGER, or LPAREN" << std::endl;
        exit(1);
    }
}

// <Identifier> -> IDENTIFIER_TOKEN
void ParserClass::Identifier() {
    Match(IDENTIFIER_TOKEN);
}

// <Integer> -> INTEGER_TOKEN
void ParserClass::Integer() {
    Match(INTEGER_TOKEN);
}

// The Match() method
TokenClass ParserClass::Match(TokenType expectedType) {
    TokenClass currentToken = mScanner->GetNextToken();
    if(currentToken.GetTokenType() != expectedType) {
        std::cerr << "Error in ParserClass::Match. " << std::endl;
        std::cerr << "Expected token type " << TokenClass::GetTokenTypeName(expectedType)
                  << ", but got type " << currentToken.GetTokenTypeName()
                  << " (\"" << currentToken.GetLexeme() << "\")" << std::endl;
        exit(1);
    }
    MSG("Matched " << currentToken.GetTokenTypeName() << " : \"" << currentToken.GetLexeme() << "\"");
    return currentToken;
}
