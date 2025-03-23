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
class MinusNode;


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


class StatementNode : public Node {
    public:
        virtual ~StatementNode();
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

    
class BlockNode : public StatementNode {
    public:
        BlockNode(StatementGroupNode* statementGroup);
        virtual ~BlockNode();
        StatementGroupNode* GetStatementGroup() const;
    private:
        StatementGroupNode* mStatementGroup;
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


class SymbolTableClass;
class IdentifierNode : public ExpressionNode {
public:
    // The constructor takes a label and a symbol table pointer
    IdentifierNode(const std::string& label, SymbolTableClass* symbolTable);
    virtual ~IdentifierNode();
    virtual int Evaluate() const override;
    void DeclareVariable();
    void SetValue(int v);
    int GetIndex() const;
private:
    std::string mLabel;
    SymbolTableClass* mSymbolTable;
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


class MinusNode : public BinaryOperatorNode {
public:
    MinusNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~MinusNode();
    virtual int Evaluate() const override;
};


class TimesNode : public BinaryOperatorNode {
public:
    TimesNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~TimesNode();
    virtual int Evaluate() const override;
};


class DivideNode : public BinaryOperatorNode {
public:
    DivideNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~DivideNode();
    virtual int Evaluate() const override;
};


// Relational operator nodes

class LessNode : public BinaryOperatorNode {
    public:
        LessNode(ExpressionNode* left, ExpressionNode* right);
        virtual ~LessNode();
        virtual int Evaluate() const override;
    };


class LessEqualNode : public BinaryOperatorNode {
public:
    LessEqualNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~LessEqualNode();
    virtual int Evaluate() const override;
};


class GreaterNode : public BinaryOperatorNode {
public:
    GreaterNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~GreaterNode();
    virtual int Evaluate() const override;
};


class GreaterEqualNode : public BinaryOperatorNode {
public:
    GreaterEqualNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~GreaterEqualNode();
    virtual int Evaluate() const override;
};


class EqualNode : public BinaryOperatorNode {
public:
    EqualNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~EqualNode();
    virtual int Evaluate() const override;
};


class NotEqualNode : public BinaryOperatorNode {
public:
    NotEqualNode(ExpressionNode* left, ExpressionNode* right);
    virtual ~NotEqualNode();
    virtual int Evaluate() const override;
};
