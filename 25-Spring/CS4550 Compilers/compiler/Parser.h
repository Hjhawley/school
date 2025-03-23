#pragma once

#include "Scanner.h"
#include "Symbol.h"

class ParserClass {
public:
    // Constructor saves pointers to your scanner and symbol table
    ParserClass(ScannerClass *scanner, SymbolTableClass *symTable);

    // The main driver: checks if the tokens from Scanner form a valid program
    void Start();

private:
    // Pointers to existing objects (not owned by ParserClass)
    ScannerClass *mScanner;
    SymbolTableClass *mSymbolTable;

    // Helper methods matching your grammar:
    // <Start> → <Program> ENDFILE_TOKEN
    void StartRule();

    // <Program> → VOID MAIN LPAREN RPAREN <Block>
    void Program();

    // <Block> → LCURLY_TOKEN <StatementGroup> RCURLY_TOKEN
    void Block();

    // <StatementGroup> → <Statement> <StatementGroup> | {empty}
    void StatementGroup();

    // <Statement> → <DeclarationStatement> | <AssignmentStatement> | <CoutStatement> | <Block>
    bool Statement();  // returns true if it recognized a statement, false otherwise

    // <DeclarationStatement> → INT <Identifier> SEMICOLON
    void DeclarationStatement();

    // <AssignmentStatement> → <Identifier> ASSIGNMENT <Expression> SEMICOLON
    void AssignmentStatement();

    // <CoutStatement> → COUT INSERTION <Expression> SEMICOLON
    void CoutStatement();

    // <Expression> → <Relational>
    // We'll do the sub-rules: Relational → ...
    void Expression(); // or use a hierarchy: Expression() → Relational()

    void Relational();
    void PlusMinus();
    void TimesDivide();
    void Factor();
    void Identifier();
    void Integer();

    // Matches a token of the expected type or exits if mismatch
    TokenClass Match(TokenType expected);
};
