#include "Node.h"
#include "Symbol.h"
#include <cstdlib>

Node::~Node() {}


StartNode::StartNode(ProgramNode* program)
    : mProgram(program) {
}

StartNode::~StartNode() {
    delete mProgram;
}

ProgramNode* StartNode::GetProgram() const {
    return mProgram;
}


ProgramNode::ProgramNode(BlockNode* block)
    : mBlock(block) {
}

ProgramNode::~ProgramNode() {
    delete mBlock;
}

BlockNode* ProgramNode::GetBlock() const {
    return mBlock;
}


BlockNode::BlockNode(StatementGroupNode* statementGroup)
    : mStatementGroup(statementGroup) {
}

BlockNode::~BlockNode() {
    delete mStatementGroup;
}

StatementGroupNode* BlockNode::GetStatementGroup() const {
    return mStatementGroup;
}


StatementGroupNode::StatementGroupNode() {}

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

StatementNode::~StatementNode() {}


DeclarationStatementNode::DeclarationStatementNode(IdentifierNode* identifier)
    : mIdentifier(identifier) {
}

DeclarationStatementNode::~DeclarationStatementNode() {
    delete mIdentifier;
}

IdentifierNode* DeclarationStatementNode::GetIdentifier() const {
    return mIdentifier;
}


AssignmentStatementNode::AssignmentStatementNode(IdentifierNode* identifier, ExpressionNode* expression)
    : mIdentifier(identifier), mExpression(expression) {
}

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


CoutStatementNode::CoutStatementNode(ExpressionNode* expression)
    : mExpression(expression) {
}

CoutStatementNode::~CoutStatementNode() {
    delete mExpression;
}

ExpressionNode* CoutStatementNode::GetExpression() const {
    return mExpression;
}


ExpressionNode::~ExpressionNode() {}


IntegerNode::IntegerNode(int value)
    : mValue(value) {
}

IntegerNode::~IntegerNode() {}

int IntegerNode::Evaluate() const {
    return mValue;
}


IdentifierNode::IdentifierNode(const std::string& label, SymbolTableClass* symbolTable)
    : mLabel(label), mSymbolTable(symbolTable) { }

IdentifierNode::~IdentifierNode() { }

int IdentifierNode::Evaluate() const {
    return mSymbolTable->GetValue(mLabel);
}

void IdentifierNode::DeclareVariable() {
    mSymbolTable->AddEntry(mLabel);
}

void IdentifierNode::SetValue(int v) {
    mSymbolTable->SetValue(mLabel, v);
}

int IdentifierNode::GetIndex() const {
    return mSymbolTable->GetIndex(mLabel);
}


BinaryOperatorNode::BinaryOperatorNode(ExpressionNode* left, ExpressionNode* right)
    : mLeft(left), mRight(right) {
}

BinaryOperatorNode::~BinaryOperatorNode() {
    delete mLeft;
    delete mRight;
}


PlusNode::PlusNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

PlusNode::~PlusNode() {}

int PlusNode::Evaluate() const {
    return mLeft->Evaluate() + mRight->Evaluate();
}


MinusNode::MinusNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

MinusNode::~MinusNode() {}

int MinusNode::Evaluate() const {
    return mLeft->Evaluate() - mRight->Evaluate();
}


TimesNode::TimesNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right)
{
}

TimesNode::~TimesNode() {}

int TimesNode::Evaluate() const {
    return mLeft->Evaluate() * mRight->Evaluate();
}


DivideNode::DivideNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right)
{
}

DivideNode::~DivideNode() {}

int DivideNode::Evaluate() const {
    int rightVal = mRight->Evaluate();
    // Your assignment might expect integer division. 
    // Handle divide-by-zero logic if you wish.
    return mLeft->Evaluate() / rightVal;
}
