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


class Node {
public:
    virtual ~Node();
};


// Nonterminal nodes

class StartNode : public Node {
public:
    StartNode(ProgramNode* program);
    virtual ~StartNode();
    ProgramNode* GetProgram() const;
private:
    ProgramNode* mProgram;
};


class ProgramNode : public Node {
public:
    ProgramNode(BlockNode* block);
    virtual ~ProgramNode();
    BlockNode* GetBlock() const;
private:
    BlockNode* mBlock;
};


class BlockNode : public Node {
public:
    BlockNode(StatementGroupNode* statementGroup);
    virtual ~BlockNode();
    StatementGroupNode* GetStatementGroup() const;
private:
    StatementGroupNode* mStatementGroup;
};


class StatementGroupNode : public Node {
public:
    StatementGroupNode();
    virtual ~StatementGroupNode();
    void AddStatement(StatementNode* stmt);
    const std::vector<StatementNode*>& GetStatements() const;
private:
    std::vector<StatementNode*> mStatements;
};


class StatementNode : public Node {
public:
    virtual ~StatementNode();
};


class DeclarationStatementNode : public StatementNode {
public:
    DeclarationStatementNode(IdentifierNode* identifier);
    virtual ~DeclarationStatementNode();
    IdentifierNode* GetIdentifier() const;
private:
    IdentifierNode* mIdentifier;
};


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


class CoutStatementNode : public StatementNode {
public:
    CoutStatementNode(ExpressionNode* expression);
    virtual ~CoutStatementNode();
    ExpressionNode* GetExpression() const;
private:
    ExpressionNode* mExpression;
};


// Expression nodes

class ExpressionNode {
public:
    virtual ~ExpressionNode();
    virtual int Evaluate() const = 0;
};


class IntegerNode : public ExpressionNode {
public:
    IntegerNode(int value);
    virtual ~IntegerNode();
    virtual int Evaluate() const;
private:
    int mValue;
};


class IdentifierNode : public ExpressionNode {
public:
    IdentifierNode(const std::string& label);
    virtual ~IdentifierNode();
    virtual int Evaluate() const;
    void DeclareVariable();
    void SetValue(int v);
    int GetIndex() const;
private:
    std::string mLabel;
};


//  Binary operator nodes

class BinaryOperatorNode : public ExpressionNode {
public:
    BinaryOperatorNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~BinaryOperatorNode();
protected:
    ExpressionNode* mLeft;
    ExpressionNode* mRight;
};


class PlusNode : public BinaryOperatorNode {
public:
    PlusNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~PlusNode();
    virtual int Evaluate() const;
};
