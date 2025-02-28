#include "Node.h"
#include "Symbol.h" // For IdentifierNode methods, if needed.
#include <cstdlib>

// ---------------- Node ----------------
Node::~Node() { }

// ---------------- StartNode ----------------
StartNode::StartNode(ProgramNode* program)
    : mProgram(program) { }

StartNode::~StartNode() {
    delete mProgram;
}

ProgramNode* StartNode::GetProgram() const {
    return mProgram;
}

// ---------------- ProgramNode ----------------
ProgramNode::ProgramNode(BlockNode* block)
    : mBlock(block) { }

ProgramNode::~ProgramNode() {
    delete mBlock;
}

BlockNode* ProgramNode::GetBlock() const {
    return mBlock;
}

// ---------------- BlockNode ----------------
BlockNode::BlockNode(StatementGroupNode* statementGroup)
    : mStatementGroup(statementGroup) { }

BlockNode::~BlockNode() {
    delete mStatementGroup;
}

StatementGroupNode* BlockNode::GetStatementGroup() const {
    return mStatementGroup;
}

// ---------------- StatementGroupNode ----------------
StatementGroupNode::StatementGroupNode() { }

StatementGroupNode::~StatementGroupNode() {
    for (size_t i = 0; i < mStatements.size(); i++) {
        delete mStatements[i];
    }
}

void StatementGroupNode::AddStatement(StatementNode* stmt) {
    mStatements.push_back(stmt);
}

const std::vector<StatementNode*>& StatementGroupNode::GetStatements() const {
    return mStatements;
}

// ---------------- StatementNode ----------------
StatementNode::~StatementNode() { }

// ---------------- DeclarationStatementNode ----------------
DeclarationStatementNode::DeclarationStatementNode(IdentifierNode* identifier)
    : mIdentifier(identifier) { }

DeclarationStatementNode::~DeclarationStatementNode() {
    delete mIdentifier;
}

IdentifierNode* DeclarationStatementNode::GetIdentifier() const {
    return mIdentifier;
}

// ---------------- AssignmentStatementNode ----------------
AssignmentStatementNode::AssignmentStatementNode(IdentifierNode* identifier, ExpressionNode* expression)
    : mIdentifier(identifier), mExpression(expression) { }

AssignmentStatementNode::~AssignmentStatementNode() {
    delete mIdentifier;
    delete mExpression;
}

IdentifierNode* AssignmentStatementNode::GetIdentifier() const {
    return mIdentifier;
}

ExpressionNode* AssignmentStatementNode::GetExpression() const {
    return mExpression;
}

// ---------------- CoutStatementNode ----------------
CoutStatementNode::CoutStatementNode(ExpressionNode* expression)
    : mExpression(expression) { }

CoutStatementNode::~CoutStatementNode() {
    delete mExpression;
}

ExpressionNode* CoutStatementNode::GetExpression() const {
    return mExpression;
}

// ---------------- ExpressionNode ----------------
ExpressionNode::~ExpressionNode() { }

// ---------------- IntegerNode ----------------
IntegerNode::IntegerNode(int value)
    : mValue(value) { }

IntegerNode::~IntegerNode() { }

int IntegerNode::Evaluate() const {
    return mValue;
}

// ---------------- IdentifierNode ----------------
IdentifierNode::IdentifierNode(const std::string& label)
    : mLabel(label) { }

IdentifierNode::~IdentifierNode() { }

int IdentifierNode::Evaluate() const {
    // For now, return a dummy value; later, use the symbol table.
    return 0;
}

void IdentifierNode::DeclareVariable() {
    // Implementation: call symbol table's AddEntry using mLabel.
}

void IdentifierNode::SetValue(int v) {
    // Implementation: call symbol table's SetValue using mLabel.
}

int IdentifierNode::GetIndex() const {
    // Implementation: return symbol table's index for mLabel.
    return -1;
}

// ---------------- BinaryOperatorNode ----------------
BinaryOperatorNode::BinaryOperatorNode(ExpressionNode* left, ExpressionNode* right)
    : mLeft(left), mRight(right) { }

BinaryOperatorNode::~BinaryOperatorNode() {
    delete mLeft;
    delete mRight;
}

// ---------------- PlusNode ----------------
PlusNode::PlusNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) { }

PlusNode::~PlusNode() { }

int PlusNode::Evaluate() const {
    return mLeft->Evaluate() + mRight->Evaluate();
}
