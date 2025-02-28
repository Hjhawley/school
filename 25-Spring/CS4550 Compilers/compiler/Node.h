#pragma once
#include <string>
#include <vector>

// Forward declarations for all node classes.
class Node;
class StartNode;
class ProgramNode;
class BlockNode;
class StatementGroupNode;
class StatementNode;
class DeclarationStatementNode;
class AssignmentStatementNode;
class CoutStatementNode;
class ExpressionNode;
class IdentifierNode;
class IntegerNode;
class BinaryOperatorNode;
class PlusNode;
// (Add additional operators as needed, e.g., MinusNode, TimesNode, DivideNode, etc.)

// Abstract base class for all nodes.
class Node {
public:
    virtual ~Node(); // Virtual destructor for proper cleanup.
};

// --- Nonterminal nodes ---

// <Start> → <Program> ENDFILE
class StartNode : public Node {
public:
    StartNode(ProgramNode* program);
    virtual ~StartNode();

    ProgramNode* GetProgram() const;
private:
    ProgramNode* mProgram;
};

// <Program> → VOID MAIN LPAREN RPAREN <Block>
class ProgramNode : public Node {
public:
    ProgramNode(BlockNode* block);
    virtual ~ProgramNode();

    BlockNode* GetBlock() const;
private:
    BlockNode* mBlock;
};

// <Block> → LCURLY <StatementGroup> RCURLY
class BlockNode : public Node {
public:
    BlockNode(StatementGroupNode* statementGroup);
    virtual ~BlockNode();

    StatementGroupNode* GetStatementGroup() const;
private:
    StatementGroupNode* mStatementGroup;
};

// <StatementGroup> → (a sequence of statements)
class StatementGroupNode : public Node {
public:
    StatementGroupNode();
    virtual ~StatementGroupNode();

    // Add a StatementNode pointer to the group.
    void AddStatement(StatementNode* stmt);
    const std::vector<StatementNode*>& GetStatements() const;
private:
    std::vector<StatementNode*> mStatements;
};

// --- Abstract base for statements ---
class StatementNode : public Node {
public:
    virtual ~StatementNode();
};

// <DeclarationStatement> → INT <Identifier> SEMICOLON
class DeclarationStatementNode : public StatementNode {
public:
    DeclarationStatementNode(IdentifierNode* identifier);
    virtual ~DeclarationStatementNode();

    IdentifierNode* GetIdentifier() const;
private:
    IdentifierNode* mIdentifier;
};

// <AssignmentStatement> → <Identifier> ASSIGNMENT <Expression> SEMICOLON
class AssignmentStatementNode : public StatementNode {
public:
    AssignmentStatementNode(IdentifierNode* identifier, ExpressionNode* expression);
    virtual ~AssignmentStatementNode();

    IdentifierNode* GetIdentifier() const;
    ExpressionNode* GetExpression() const;
private:
    IdentifierNode* mIdentifier;
    ExpressionNode* mExpression;
};

// <CoutStatement> → COUT INSERTION <Expression> SEMICOLON
class CoutStatementNode : public StatementNode {
public:
    CoutStatementNode(ExpressionNode* expression);
    virtual ~CoutStatementNode();

    ExpressionNode* GetExpression() const;
private:
    ExpressionNode* mExpression;
};

// --- Expression nodes ---
// Abstract base class for expressions.
class ExpressionNode {
public:
    virtual ~ExpressionNode();
    // Evaluate the expression and return its integer value.
    virtual int Evaluate() const = 0;
};

// <Integer> → INTEGER
class IntegerNode : public ExpressionNode {
public:
    IntegerNode(int value);
    virtual ~IntegerNode();
    virtual int Evaluate() const;
private:
    int mValue;
};

// <Identifier> → IDENTIFIER
// (In a complete system, an IdentifierNode would also hold a pointer to the symbol table.)
class IdentifierNode : public ExpressionNode {
public:
    IdentifierNode(const std::string& label);
    virtual ~IdentifierNode();
    virtual int Evaluate() const;
    
    // For interpretation purposes.
    void DeclareVariable();
    void SetValue(int v);
    int GetIndex() const;
private:
    std::string mLabel;
    // SymbolTableClass* mSymbolTable; // (Assume this is set externally.)
};

// --- Binary operator nodes ---
// Abstract base for binary operators.
class BinaryOperatorNode : public ExpressionNode {
public:
    BinaryOperatorNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~BinaryOperatorNode();
protected:
    ExpressionNode* mLeft;
    ExpressionNode* mRight;
};

// <Expression> → <Expression> PLUS <Expression>
class PlusNode : public BinaryOperatorNode {
public:
    PlusNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~PlusNode();
    virtual int Evaluate() const;
};
