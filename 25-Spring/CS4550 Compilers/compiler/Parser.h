#pragma once

#include "Scanner.h"
#include "Symbol.h"
#include "Node.h"

class ParserClass {
public:
    ParserClass(ScannerClass *scanner, SymbolTableClass *symTable);

    // Now returns a StartNode pointer
    StartNode* Start();

private:
    ScannerClass *mScanner;
    SymbolTableClass *mSymbolTable;

    // <Start> → <Program> ENDFILE
    StartNode* StartRule();

    // <Program> → VOID MAIN LPAREN RPAREN <Block>
    ProgramNode* Program();

    // <Block> → LCURLY <StatementGroup> RCURLY
    // Our BlockNode might derive from StatementNode, but we return BlockNode* for clarity
    BlockNode* Block();

    // <StatementGroup> → {empty} | <Statement> <StatementGroup>
    StatementGroupNode* StatementGroup();

    // <Statement> -> <DeclarationStatement> | <AssignmentStatement> | <CoutStatement> | <Block>
    // Return nullptr if no statement recognized
    StatementNode* Statement();

    // <DeclarationStatement> → INT <Identifier> SEMICOLON
    DeclarationStatementNode* DeclarationStatement();

    // <AssignmentStatement> → <Identifier> ASSIGNMENT <Expression> SEMICOLON
    AssignmentStatementNode* AssignmentStatement();

    // <IfStatement> -> IF LPAREN <Expression> RPAREN <Statement>
    StatementNode* IfStatement();

    // <CoutStatement> → COUT INSERTION <Expression> SEMICOLON
    CoutStatementNode* CoutStatement();

    // <Expression> -> <Relational>
    ExpressionNode* Expression();

    // <Relational> -> <PlusMinus> [ one relational operator <PlusMinus> ]
    ExpressionNode* Relational();

    // <PlusMinus> -> <TimesDivide> { ( + | - ) <TimesDivide> }
    ExpressionNode* PlusMinus();

    // <TimesDivide> -> <Factor> { ( * | / ) <Factor> }
    ExpressionNode* TimesDivide();

    // <Factor> -> <Identifier> | <Integer> | LPAREN <Expression> RPAREN
    ExpressionNode* Factor();

    // <Identifier> -> IDENTIFIER_TOKEN
    IdentifierNode* Identifier();

    // <Integer> -> INTEGER_TOKEN
    IntegerNode* Integer();

    // Match a token or exit on error
    TokenClass Match(TokenType expected);
};
