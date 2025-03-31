#include "Parser.h"
#include "Debug.h"
#include <cstdlib>  // for exit
#include <iostream> // for error messages
#include <cstdio>   // for atoi or use stoi in C++11

ParserClass::ParserClass(ScannerClass *scanner, SymbolTableClass *symTable)
    : mScanner(scanner), mSymbolTable(symTable) {
}

// Start() – returns a StartNode pointer
StartNode* ParserClass::Start() {
    // Use a helper "StartRule()" which returns StartNode
    StartNode* sn = StartRule();
    return sn;
}

// <Start> → <Program> ENDFILE
StartNode* ParserClass::StartRule() {
    ProgramNode* pn = Program();
    Match(ENDFILE_TOKEN);
    // Construct the StartNode from the ProgramNode
    StartNode* sn = new StartNode(pn);
    return sn;
}

// <Program> → VOID MAIN LPAREN RPAREN <Block>
ProgramNode* ParserClass::Program() {
    Match(VOID_TOKEN);
    Match(MAIN_TOKEN);
    Match(LPAREN_TOKEN);
    Match(RPAREN_TOKEN);

    // Grab a BlockNode from Block()
    BlockNode* block = Block();
    // Make a ProgramNode holding that block
    ProgramNode* pn = new ProgramNode(block);
    return pn;
}

// <Block> → LCURLY <StatementGroup> RCURLY
BlockNode* ParserClass::Block() {
    Match(LCURLY_TOKEN);
    StatementGroupNode* sg = StatementGroup();
    Match(RCURLY_TOKEN);
    return new BlockNode(sg);
}

// <StatementGroup> → {empty} | <Statement> <StatementGroup>
StatementGroupNode* ParserClass::StatementGroup() {
    StatementGroupNode* sg = new StatementGroupNode();
    while(true) {
        // See if we can parse a statement
        StatementNode* stmt = Statement();
        if(stmt == nullptr) {
            break; // no statement found
        }
        // Add it
        sg->AddStatement(stmt);
    }
    return sg;
}

// <Statement> -> <DeclarationStatement> | <AssignmentStatement> | <CoutStatement> | <Block>
StatementNode* ParserClass::Statement() {
    // Peek to see what we have
    TokenType tt = mScanner->PeekNextToken().GetTokenType();
    if(tt == INT_TOKEN) {
        return DeclarationStatement();
    }
    else if(tt == IDENTIFIER_TOKEN) {
        return AssignmentStatement();
    }
    else if(tt == COUT_TOKEN) {
        return CoutStatement();
    }
    else if(tt == LCURLY_TOKEN) {
        // a block is also a StatementNode
        return Block();
    }
    // no statement recognized
    return nullptr;
}

// <DeclarationStatement> -> INT <Identifier> SEMICOLON
DeclarationStatementNode* ParserClass::DeclarationStatement() {
    Match(INT_TOKEN);
    IdentifierNode* idNode = Identifier();
    ExpressionNode* initExpr = nullptr; // default, if just a semicolon
    TokenType tt = mScanner->PeekNextToken().GetTokenType(); // peek to check if ASSIGNMENT or SEMICOLON
    if(tt == ASSIGNMENT_TOKEN) {
        Match(ASSIGNMENT_TOKEN);  // consume =
        initExpr = Expression();  // "x - 3"
    }
    // otherwise we just saw a semicolon
    Match(SEMICOLON_TOKEN);
    return new DeclarationStatementNode(idNode, initExpr);
}

// <AssignmentStatement> -> <Identifier> ASSIGNMENT <Expression> SEMICOLON
AssignmentStatementNode* ParserClass::AssignmentStatement() {
    IdentifierNode* id = Identifier();
    Match(ASSIGNMENT_TOKEN);
    ExpressionNode* expr = Expression();
    Match(SEMICOLON_TOKEN);

    // Return a node
    return new AssignmentStatementNode(id, expr);
}

// <CoutStatement> -> COUT INSERTION <Expression> SEMICOLON
CoutStatementNode* ParserClass::CoutStatement() {
    Match(COUT_TOKEN);
    Match(INSERTION_TOKEN); // <<
    ExpressionNode* expr = Expression();
    Match(SEMICOLON_TOKEN);

    return new CoutStatementNode(expr);
}

// <Expression> -> <Relational>
ExpressionNode* ParserClass::Expression() {
    return Relational();
}

// <Relational> -> <PlusMinus> [ a single relational operator <PlusMinus> ]
ExpressionNode* ParserClass::Relational() {
    ExpressionNode* current = PlusMinus();

    TokenType tt = mScanner->PeekNextToken().GetTokenType();
    if(tt == LESS_TOKEN || tt == LESSEQUAL_TOKEN ||
       tt == GREATER_TOKEN || tt == GREATEREQUAL_TOKEN ||
       tt == EQUAL_TOKEN || tt == NOTEQUAL_TOKEN)
    {
        // match the operator
        Match(tt);
        // parse the right subexpression
        ExpressionNode* right = PlusMinus();

        switch(tt) {
            case LESS_TOKEN: return new LessNode(current, right);
            case LESSEQUAL_TOKEN: return new LessEqualNode(current, right);
            case GREATER_TOKEN: return new GreaterNode(current, right);
            case GREATEREQUAL_TOKEN: return new GreaterEqualNode(current, right);
            case EQUAL_TOKEN: return new EqualNode(current, right);
            case NOTEQUAL_TOKEN: return new NotEqualNode(current, right);
            default: /* impossible */ break;
        }
    }
    return current;
}

// <PlusMinus> -> <TimesDivide> { ( + | - ) <TimesDivide> }
ExpressionNode* ParserClass::PlusMinus() {
    // parse the first subexpression
    ExpressionNode* current = TimesDivide();
    while(true) {
        TokenType tt = mScanner->PeekNextToken().GetTokenType();
        if(tt == PLUS_TOKEN) {
            Match(PLUS_TOKEN);
            ExpressionNode* right = TimesDivide();
            current = new PlusNode(current, right);
        }
        else if(tt == MINUS_TOKEN) {
            Match(MINUS_TOKEN);
            ExpressionNode* right = TimesDivide();
            current = new MinusNode(current, right);
        }
        else {
            // no more plus/minus
            break;
        }
    }
    return current;
}

// <TimesDivide> -> <Factor> { ( * | / ) <Factor> }
ExpressionNode* ParserClass::TimesDivide() {
    ExpressionNode* current = Factor();
    while(true) {
        TokenType tt = mScanner->PeekNextToken().GetTokenType();
        if(tt == TIMES_TOKEN) {
            Match(TIMES_TOKEN);
            ExpressionNode* right = Factor();
            current = new TimesNode(current, right);
        }
        else if(tt == DIVIDE_TOKEN) {
            Match(DIVIDE_TOKEN);
            ExpressionNode* right = Factor();
            current = new DivideNode(current, right);
        }
        else {
            break;
        }
    }
    return current;
}

// <Factor> -> <Identifier> | <Integer> | LPAREN <Expression> RPAREN
ExpressionNode* ParserClass::Factor() {
    TokenType tt = mScanner->PeekNextToken().GetTokenType();
    if(tt == IDENTIFIER_TOKEN) {
        return Identifier();
    }
    else if(tt == INTEGER_TOKEN) {
        return Integer();
    }
    else if(tt == LPAREN_TOKEN) {
        Match(LPAREN_TOKEN);
        ExpressionNode* expr = Expression();
        Match(RPAREN_TOKEN);
        return expr;
    }
    else {
        std::cerr << "Error in Factor(): Expected IDENTIFIER, INTEGER, or LPAREN" << std::endl;
        exit(1);
    }
}

// <Identifier> -> IDENTIFIER_TOKEN
IdentifierNode* ParserClass::Identifier() {
    TokenClass tk = Match(IDENTIFIER_TOKEN);
    // Build an IdentifierNode using the lexeme from the token
    std::string label = tk.GetLexeme();
    return new IdentifierNode(label, mSymbolTable);
}

// <Integer> -> INTEGER_TOKEN
IntegerNode* ParserClass::Integer() {
    TokenClass tk = Match(INTEGER_TOKEN);
    std::string lex = tk.GetLexeme();
    int val = std::atoi(lex.c_str()); // or std::stoi(lex)
    return new IntegerNode(val);
}

// The Match() method remains the same except for returning the matched token
TokenClass ParserClass::Match(TokenType expectedType) {
    TokenClass currentToken = mScanner->GetNextToken();
    if(currentToken.GetTokenType() != expectedType) {
        std::cerr << "Error in ParserClass::Match: expected "
                  << TokenClass::GetTokenTypeName(expectedType) << " but got "
                  << currentToken.GetTokenTypeName() << " (\""
                  << currentToken.GetLexeme() << "\")" << std::endl;
        exit(1);
    }
    MSG("Matched " << currentToken.GetTokenTypeName()
        << " : \"" << currentToken.GetLexeme() << "\"");
    return currentToken;
}
